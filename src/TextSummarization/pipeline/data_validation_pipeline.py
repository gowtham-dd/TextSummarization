from src.TextSummarization.config.configuration import ConfigurationManager
from src.TextSummarization.components.data_validation import DataValiadtion
from src.TextSummarization import logger


STAGE_NAME="Data Ingestion stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
          
        try:
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValiadtion(config=data_validation_config)
            data_validation.validate_all_files_exist()
        except Exception as e:
            raise e


if __name__ == "__main__":
     try:
          logger.info(f">>>> Stage {STAGE_NAME} started")
          obj=DataValidationTrainingPipeline()
          obj.main()
          logger.info(f">>>>> Stage {STAGE_NAME} completed")

     except Exception as e:
          logger.exception(e)
          raise e
