import os
from pathlib import Path
import pandas as pd
from tqdm import tqdm
import evaluate
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk
from src.TextSummarization.entity.config_entity import ModelEvaluationConfig
import torch


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
        # Convert to Path objects if they aren't already
        self.metrics_file = Path(self.config.metric_file_name)
        self.data_path = Path(self.config.data_path)
        self.model_path = Path(self.config.model_path)
        self.tokenizer_path = Path(self.config.tokenizer_path)

    def generate_batch_sized_chunks(self, list_of_elements, batch_size):
        """Split the dataset into smaller batches"""
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i : i + batch_size]

    def calculate_metric_on_test_ds(self, dataset, metric, model, tokenizer, 
                                 batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu", 
                                 column_text="dialogue", 
                                 column_summary="summary"):
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

        for article_batch, target_batch in tqdm(
            zip(article_batches, target_batches), total=len(article_batches)):
            
            inputs = tokenizer(article_batch, max_length=1024, truncation=True, 
                            padding="max_length", return_tensors="pt")
            
            summaries = model.generate(
                input_ids=inputs["input_ids"].to(device),
                attention_mask=inputs["attention_mask"].to(device),
                length_penalty=0.8, 
                num_beams=8, 
                max_length=128
            )
            
            decoded_summaries = [
                tokenizer.decode(s, skip_special_tokens=True, clean_up_tokenization_spaces=True) 
                for s in summaries
            ]
            
            metric.add_batch(predictions=decoded_summaries, references=target_batch)
            
        return metric.compute()

    def evaluate(self):
        # Check if metrics file already exists
        if self.metrics_file.exists():
            print(f"✅ Metrics file {self.metrics_file} already exists. Skipping evaluation...")
            return
            
        print("Starting evaluation...")
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(str(self.tokenizer_path))
        model = AutoModelForSeq2SeqLM.from_pretrained(str(self.model_path)).to(device)
       
        # Load dataset
        dataset = load_from_disk(str(self.data_path))

        # Initialize ROUGE metric
        try:
            rouge_metric = evaluate.load('rouge')
        except:
            from rouge_score import rouge_scorer
            rouge_metric = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

        # Evaluate on first 10 samples
        score = self.calculate_metric_on_test_ds(
            dataset['test'][0:10], 
            rouge_metric, 
            model, 
            tokenizer, 
            batch_size=2, 
            column_text='dialogue', 
            column_summary='summary'
        )

        # Process results
        if hasattr(score, 'items'):  # evaluate format
            rouge_dict = {
                'rouge1': score['rouge1'].mid.fmeasure,
                'rouge2': score['rouge2'].mid.fmeasure,
                'rougeL': score['rougeL'].mid.fmeasure,
                'rougeLsum': score['rougeLsum'].mid.fmeasure
            }
        else:  # rouge_scorer format
            rouge_dict = {
                'rouge1': score['rouge1'].fmeasure,
                'rouge2': score['rouge2'].fmeasure,
                'rougeL': score['rougeL'].fmeasure,
                'rougeLsum': score['rougeL'].fmeasure  # Approximation
            }

        # Save results
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rouge_dict, index=['pegasus']).to_csv(self.metrics_file, index=False)
        print(f"✅ Evaluation completed. Metrics saved to {self.metrics_file}")