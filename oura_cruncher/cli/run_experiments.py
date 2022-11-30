from datetime import time

import click
from scipy.stats import describe

from ..models.night import Night
from ..utils import hour_to_seconds, time_to_seconds
from ..experiments.ttest import ttest


def select_night(night: Night, bedtime_hour: int) -> bool:
    bedtime_hour_seconds = hour_to_seconds(bedtime_hour)
    lower_bound_seconds = bedtime_hour_seconds - 15 * 60
    upper_bound_seconds = bedtime_hour_seconds + 15 * 60
    bedtime = night.corrected_bedtime_start
    return not night.reject_reason and lower_bound_seconds < time_to_seconds(bedtime) <= upper_bound_seconds


@click.command
def run_experiments():
    nights = Night.get_nights_from_sheets()
    nights_a = [night for night in nights if select_night(night, 23)]
    nights_b = [night for night in nights if select_night(night, 24)]

    print(describe([night.corrected_efficiency for night in nights_a]))
    print(describe([night.corrected_efficiency for night in nights_b]))
    print(ttest(nights_a, nights_b))
