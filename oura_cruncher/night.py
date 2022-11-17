from functools import cache
from pathlib import Path
from datetime import date
from itertools import groupby

from pydantic import BaseModel
from oura.v2 import OuraClientV2


@cache
def get_client():
    token = Path(".token").read_text().strip()
    return OuraClientV2(personal_access_token=token)


class Night(BaseModel):
    day: str
    period: int
    total_sleep_duration: int
    time_in_bed: int

    @property
    def efficiency(self):
        return self.total_sleep_duration / self.time_in_bed

    @classmethod
    def get_nights(cls, start_date: str = "2022-11-12", end_date: str | None = None):
        if not end_date:
            end_date = date.today().isoformat()

        client = get_client()
        data = client._get_summary(start_date, end_date, None, "sleep")["data"]
        sleep_periods = (cls.parse_obj(item) for item in data)

        # only yield the longest sleep period for each day
        for _, day_sleep_periods in groupby(
            sleep_periods, lambda sleep_period: sleep_period.day
        ):
            yield max(
                day_sleep_periods,
                key=lambda sleep_period: sleep_period.total_sleep_duration,
            )
