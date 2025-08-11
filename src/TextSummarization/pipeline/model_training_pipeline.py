

from src.TextSummarization.config.configuration import ConfigurationManager
from src.TextSummarization.components.ModelTraining import ModelTrainer
from src.TextSummarization import logger


STAGE_NAME="Model TrainingPipeline stage"

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
          
        try:
            config = ConfigurationManager()
            model_trainer_config = config.get_model_trainer_config()
            model_trainer_config = ModelTrainer(config=model_trainer_config)
            model_trainer_config.train()
        except Exception as e:
            raise e


if __name__ == "__main__":
     try:
          logger.info(f">>>> Stage {STAGE_NAME} started")
          obj=ModelTrainingPipeline()
          obj.main()
          logger.info(f">>>>> Stage {STAGE_NAME} completed")

     except Exception as e:
          logger.exception(e)
          raise e
