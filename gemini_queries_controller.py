"""The gemini_queries_controller module. Simple operations for the gemini_queries table."""
# gemini_queries_controller.py
# pylint: disable=line-too-long

import logging
from sqlalchemy import Table, MetaData, select, insert, delete
from sqlalchemy.exc import SQLAlchemyError
from db import db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

gemini_queries = Table('gemini_queries', MetaData(), autoload_with=db.engine)

def fetch_gemini_queries(limit: int = 10) -> list:
    """
    Retrieve the latest <limit#> of user queries from the database.

    Parameters:
    limit (int): The maximum number of queries to return. Defaults to 10.

    Returns:
    list: A list of the latest <limit#> of queries represented as dictionaries.

    Raises:
    SQLAlchemyError: If an error occurs while retrieving the queries from the database.
    """
    with db.get_session() as session:
        try:
            result = session.execute(select(gemini_queries).limit(limit).order_by(gemini_queries.c.created_at.desc()))
            return result.fetchall()
        except SQLAlchemyError as e:
            logger.error("Error occurred: %s", e)
            return []

def insert_gemini_query(*, original_filename: str, cloud_filename: str = '', prompt: str, response: str, ) -> None:
    """
    Insert the basic results of a gemini query into the genimi_queries table.

    Parameters:
        filename (str): The name of the image file provided to the query.
        cloud_filename (str): The name of the file in the cloud storage bucket. Defaults to an empty string.
        prompt (str): The user prompt that was provided to gemini-vision-pro.
        response (str): The text response from gemini-vision-pro.

    Raises:
        SQLAlchemyError: If an error occurs while inserting the query into the database.
    """
    with db.get_session() as session:
        try:
            session.execute(insert(gemini_queries).values(original_filename=original_filename, cloud_filename=cloud_filename, prompt=prompt, response=response))
        except SQLAlchemyError as e:
            logger.error("Error occurred: %s", e)

def delete_by_id(pkey: int) -> None:
    """
    Delete a single record from the gemini_queries table by its primary key.

    Parameters:
        pkey (int): The primary key of the record to delete.

    Raises:
        SQLAlchemyError: If an error occurs while deleting the record from the database.
    """
    with db.get_session() as session:
        try:
            session.execute(delete(gemini_queries).where(gemini_queries.c.id == pkey))
        except SQLAlchemyError as e:
            logger.error("Error occurred: %s", e)
