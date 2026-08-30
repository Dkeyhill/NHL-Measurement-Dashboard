"""
Deploys load_schedule_proc.py to Snowflake: uploads it to the DEV stage,
then (re)creates the stored procedure pointing at the staged file.

Usage (from this directory):
    python deploy.py
"""
import getpass
import os

import snowflake.connector
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

load_dotenv()

STAGE_PATH = "@RAW.INGESTION_STAGE"
PROC_SOURCE = "load_schedule_proc.py"


def load_private_key():
    key_path = os.environ["SNOWFLAKE_PRIVATE_KEY_PATH"]
    passphrase = getpass.getpass("Private key passphrase: ")

    with open(key_path, "rb") as key_file:
        p_key = serialization.load_pem_private_key(
            key_file.read(),
            password=passphrase.encode(),
        )

    return p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def get_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        private_key=load_private_key(),
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database="DEV",
        schema="RAW",
    )


def deploy():
    conn = get_connection()
    try:
        cur = conn.cursor()

        # 1. Upload source to the stage (overwrite each time you redeploy)
        cur.execute(f"PUT file://{PROC_SOURCE} {STAGE_PATH} OVERWRITE = TRUE AUTO_COMPRESS = FALSE")

        # 2. (Re)create the procedure pointing at the staged file
        cur.execute(f"""
            CREATE OR REPLACE PROCEDURE RAW.LOAD_SCHEDULE(start_date STRING)
            RETURNS STRING
            LANGUAGE PYTHON
            RUNTIME_VERSION = '3.11'
            HANDLER = 'load_schedule_proc.load_schedule'
            EXTERNAL_ACCESS_INTEGRATIONS = (NHL_API_ACCESS_INTEGRATION)
            PACKAGES = ('requests', 'snowflake-snowpark-python')
            IMPORTS = ('{STAGE_PATH}/load_schedule_proc.py')
        """)
        print("Deployed RAW.LOAD_SCHEDULE to DEV.")
    finally:
        conn.close()


if __name__ == "__main__":
    deploy()