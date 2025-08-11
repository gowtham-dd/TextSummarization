
from src.TextSummarization.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.TextSummarization import logger

STAGE_NAME="Data Ingestion stage"


try:
    logger.info(f">>>> Stage {STAGE_NAME} started")
    obj=DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>> Stage {STAGE_NAME} completed")

except Exception as e:
    logger.exception(e)
    raise e