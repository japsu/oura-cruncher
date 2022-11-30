from functools import cache
from datetime import date, datetime
from itertools import groupby
from typing import Optional, Self

from pydantic import BaseModel
from oura.v2 import OuraClientV2
from dateutil.parser import parse as parse_datetime

from ..config import config
from ..services.sheets import get_nights_data
from ..utils import time_to_seconds


@cache
def get_client():
    return OuraClientV2(personal_access_token=config.oura.token)


SHEETS_LOAD_FIELDS = ("reject_reason", "bedtime_start_correction")


class Night(BaseModel):
    day: str
    # period: int
    total_sleep_duration: int
    time_in_bed: int
    bedtime_start: str
    bedtime_end: str

    # sheets only fields
    reject_reason: Optional[str]
    bedtime_start_correction: Optional[str]

    @property
    def efficiency(self):
        return self.total_sleep_duration / self.time_in_bed

    @property
    def corrected_bedtime_start(self):
        """
        When going to bed, I'm often so restless that Oura does not consider bedtime to start
        before some time in bed has passed.
        """
        bedtime_start = parse_datetime(self.bedtime_start)

        if not self.bedtime_start_correction:
            return bedtime_start

        # FIXME correction that spans the date boundary
        bedtime_start_correction = parse_datetime(self.bedtime_start_correction).time()

        return datetime.combine(bedtime_start.date(), bedtime_start_correction).replace(tzinfo=bedtime_start.tzinfo)

    @property
    def corrected_time_in_bed(self):
        bedtime_end = time_to_seconds(parse_datetime(self.bedtime_end), cutoff_hour=16)
        bedtime_start = time_to_seconds(self.corrected_bedtime_start, cutoff_hour=8)

        return bedtime_end - bedtime_start

    @property
    def corrected_efficiency(self):
        return self.total_sleep_duration / self.corrected_time_in_bed

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
        return [cls.parse_obj(obj) for obj in get_nights_data()]

    @classmethod
    def update_nights_from_sheets(cls, nights: list[Self], sheets_data: list[dict[str, str]]):
        sheets_data_by_day = {row["day"]: row for row in sheets_data}

        for night in nights:
            if row := sheets_data_by_day.get(night.day):
                for field_name in SHEETS_LOAD_FIELDS:
                    if field_name in row:
                        setattr(night, field_name, row[field_name])

    @property
    def sheets_row(self):
        return [
            self.day,
            self.total_sleep_duration,
            self.time_in_bed,
            self.bedtime_start,
            self.bedtime_end,
            self.corrected_time_in_bed,
        ]
