import os

from dotenv import load_dotenv
from snowflake.snowpark import Session

from deploy import load_private_key

load_dotenv()


def get_local_session():
    connection_parameters = {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "private_key": load_private_key(),
        "role": os.environ["SNOWFLAKE_ROLE"],
        "warehouse": os.environ["SNOWFLAKE_WAREHOUSE"],
        "database": "DEV",
        "schema": "RAW",
    }
    return Session.builder.configs(connection_parameters).create()