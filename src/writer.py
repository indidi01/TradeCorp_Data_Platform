import logging
from utils import CLEAN_DATA_DIR

logger = logging.getLogger(__name__)

def write_clean(df):
    logger.info("Ecriture du dataframe dans clean")

    (
        df.write
        .mode("overwrite")
        .parquet(CLEAN_DATA_DIR)
    )

    logger.info("Ecriture Parquet terminée")