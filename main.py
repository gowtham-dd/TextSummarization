
from src.TextSummarization.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.TextSummarization import logger
from src.TextSummarization.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.TextSummarization.pipeline.data_transformation_pipeline import DataTransformationTrainingPipeline

STAGE_NAME="Data Ingestion stage"


try:
    logger.info(f">>>> Stage {STAGE_NAME} started")
    obj=DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>> Stage {STAGE_NAME} completed")

except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME="Data Validation stage"


try:
    logger.info(f">>>> Stage {STAGE_NAME} started")
    obj=DataValidationTrainingPipeline()
    obj.main()
    logger.info(f">>>>> Stage {STAGE_NAME} completed")

except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME="Data Transformation stage"


try:
    logger.info(f">>>> Stage {STAGE_NAME} started")
    obj=DataTransformationTrainingPipeline()
    obj.main()
    logger.info(f">>>>> Stage {STAGE_NAME} completed")

except Exception as e:
    logger.exception(e)
    raise e