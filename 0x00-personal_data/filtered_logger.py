#!/usr/bin/env python3
""" creates a filter method"""
import re
from typing import List
import logging
import mysql.connector
import os


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """ Initializes args"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Sets formats"""
        message = super().format(record)
        filter_datum(self.fields,
                     RedactingFormatter.REDACTION,
                     message, RedactingFormatter.SEPARATOR)
        return message


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Returns regex obfuscated log messages """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """Returns a logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.formatter(RedactingFormatter(list(PII_FIELDS)))
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MYSQLConnection:
    """ Establishes a connection to the db"""
    mydb = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME'),
        user=f"{os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')}",
        password=f"{os.getenv('PERSONAL_DATA_DB_PASSWORD')}"
        )
    return mydb


def main():
    """main function"""
    db_con = get_db()
    db_connect = db_con.cursor()
    db_connect.execute("SELECT * FROM users;")
    fieldz = [field[0] for field in db_connect.description]
    logger = get_logger()
    for row in db_connect:
        result = ''
        for i, j in zip(row, fieldz):
            result += f'{i}={(j)}; '
        logger.info(result)
    db_connect.close()
    db_con.close()


if __name__ == '__main__':
    main()
