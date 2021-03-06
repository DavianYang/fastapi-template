import datetime

from pydantic import BaseConfig, BaseModel

from app.utils import convert_datetime_to_realworld, convert_field_to_camel_case


class RWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}
        alias_generator = convert_field_to_camel_case
