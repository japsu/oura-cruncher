import tomllib

from pydantic import BaseModel


class OuraConfig(BaseModel):
    token: str
    start_date: str


class SheetsConfig(BaseModel):
    sheet_id: str
    range: str


class Config(BaseModel):
    oura: OuraConfig
    sheets: SheetsConfig

    @classmethod
    def load(cls):
        with open("config.toml", "rb") as input_file:
            obj = tomllib.load(input_file)

        return cls.parse_obj(obj)


config = Config.load()
