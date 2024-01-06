from datetime import datetime

from pydantic import BaseConfig


class CustomBaseConfig(BaseConfig):
    json_encoders = {datetime: lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%S%z")}
    allow_population_by_field_name = True
