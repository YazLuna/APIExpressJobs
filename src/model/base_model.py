from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from src.configuration.config_server import ConfigServer

base = declarative_base()


class BaseModel(base):
    __abstract__ = True
    connection_string = ""

    @staticmethod
    def open_connection():
        if BaseModel.connection_string == "":
            BaseModel.prepare()
        return Session(create_engine(BaseModel.connection_string))

    @staticmethod
    def prepare():
        config_server = ConfigServer("expressjobs")
        server = config_server.get("connection_string")
        BaseModel.connection_string = server.json()["connection_string"]
