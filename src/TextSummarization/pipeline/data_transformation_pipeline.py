from src.TextSummarization.config.configuration import ConfigurationManager
from src.TextSummarization.components.data_transformation import DataTransformation
from src.TextSummarization import logger


STAGE_NAME="Data Ingestion stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
          
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            data_transformation.convert()
        except Exception as e:
            raise e


if __name__ == "__main__":
     try:
          logger.info(f">>>> Stage {STAGE_NAME} started")
          obj=DataTransformationTrainingPipeline()
          obj.main()
          logger.info(f">>>>> Stage {STAGE_NAME} completed")

     except Exception as e:
          logger.exception(e)
          raise e
