from functools import cache
from datetime import date
from itertools import groupby
from typing import Optional

from pydantic import BaseModel
from oura.v2 import OuraClientV2

from .config import config
from .sheets import get_nights_data


@cache
def get_client():
    return OuraClientV2(personal_access_token=config.oura.token)


class Night(BaseModel):
    day: str
    # period: int
    total_sleep_duration: int
    time_in_bed: int

    # sheets only fields
    reject_reason: Optional[str]

    @property
    def efficiency(self):
        return self.total_sleep_duration / self.time_in_bed

    @classmethod
    def get_nights_from_oura(cls, start_date: str = config.oura.start_date, end_date: str | None = None):
        if not end_date:
            end_date = date.today().isoformat()

        client = get_client()
        data = client._get_summary(start_date, end_date, None, "sleep")["data"]
        sleep_periods = (cls.parse_obj(item) for item in data)

        # only yield the longest sleep period for each day
        for _, day_sleep_periods in groupby(sleep_periods, lambda sleep_period: sleep_period.day):
            yield max(
                day_sleep_periods,
                key=lambda sleep_period: sleep_period.total_sleep_duration,
            )

    @classmethod
    def get_nights_from_sheets(cls):
        nights_data = get_nights_data()
        return [cls.parse_obj(obj) for obj in nights_data]

    @property
    def sheets_row(self):
        return [self.day, self.total_sleep_duration, self.time_in_bed]
