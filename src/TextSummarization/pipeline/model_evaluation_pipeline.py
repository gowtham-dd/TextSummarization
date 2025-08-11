


from src.TextSummarization.config.configuration import ConfigurationManager
from src.TextSummarization.components.model_evaluation import ModelEvaluation
from src.TextSummarization import logger


STAGE_NAME="Data Ingestion stage"

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
          
        try:
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_config()
            model_evaluation_config = ModelEvaluation(config=model_evaluation_config)
            model_evaluation_config.evaluate()
        except Exception as e:
            raise e


if __name__ == "__main__":
     try:
          logger.info(f">>>> Stage {STAGE_NAME} started")
          obj=ModelEvaluationTrainingPipeline()
          obj.main()
          logger.info(f">>>>> Stage {STAGE_NAME} completed")

     except Exception as e:
          logger.exception(e)
          raise e
