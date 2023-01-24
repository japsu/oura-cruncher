from datetime import time

import click
from scipy.stats import describe

from ..models.night import Night
from ..utils import hour_to_seconds, time_to_seconds
from ..experiments.ttest import ttest


def reject_obvious(night: Night) -> bool:
    if night.reject_reason:
        return False

    if night.medication and "zolpidem" in night.medication:
        return False

    return True


def select_night_by_time_in_bed(night: Night, delta_minutes: int = 30) -> bool:
    min_in_bed_seconds = ((7 * 60) + delta_minutes) * 60  # 7h30min
    max_in_bed_seconds = ((8 * 60) + delta_minutes) * 60  # 8h30min

    return min_in_bed_seconds < night.corrected_time_in_bed < max_in_bed_seconds


def select_night_by_bedtime(night: Night, bedtime_hour: int, delta_minutes: int = 25) -> bool:
    if night.reject_reason or night.medication:
        return False

    if not select_night_by_time_in_bed(night):
        return False

    bedtime_hour_seconds = hour_to_seconds(bedtime_hour)
    min_bedtime_seconds = bedtime_hour_seconds - delta_minutes * 60
    max_bedtime_seconds = bedtime_hour_seconds + delta_minutes * 60
    bedtime_seconds = time_to_seconds(night.corrected_bedtime_start)

    return min_bedtime_seconds < bedtime_seconds <= max_bedtime_seconds


def select_night_by_doxepin(night: Night, is_doxepin: bool) -> bool:
    if night.reject_reason or night.location:
        return False

    if not select_night_by_time_in_bed(night):
        return False

    medication = night.medication or ""

    if "zolpidem" in medication:
        return False

    return ("doxepin" in medication) == is_doxepin


def select_night_by_location(night: Night, is_outside_home: bool) -> bool:
    if not reject_obvious(night):
        return False

    return bool(night.location) == is_outside_home


def select_night_by_late_sport(night: Night, late_sport: bool) -> bool:
    return select_night_by_bedtime(night, 24) and bool(night.late_sport) == late_sport


@click.command
def run_experiments():
    nights = Night.get_nights_from_sheets()

    print("Nukkumaanmenoaika 23:00 vs. 24:00")
    nights_a = [night for night in nights if select_night_by_bedtime(night, 23)]
    nights_b = [night for night in nights if select_night_by_bedtime(night, 24)]
    print(describe([night.corrected_efficiency for night in nights_a]))
    print(describe([night.corrected_efficiency for night in nights_b]))
    print(ttest(nights_a, nights_b))

    print()
    print("Ei doksepiinia vs. doksepiinilla")
    nights_a = [night for night in nights if select_night_by_doxepin(night, False)]
    nights_b = [night for night in nights if select_night_by_doxepin(night, True)]
    print(describe([night.corrected_efficiency for night in nights_a]))
    print(describe([night.corrected_efficiency for night in nights_b]))
    print(ttest(nights_a, nights_b))

    print()
    print("Kotona vs. kodin ulkopuolella")
    nights_a = [night for night in nights if select_night_by_location(night, False)]
    nights_b = [night for night in nights if select_night_by_location(night, True)]
    print(describe([night.corrected_efficiency for night in nights_a]))
    print(describe([night.corrected_efficiency for night in nights_b]))
    print(ttest(nights_a, nights_b))

    print()
    print("Ei iltaliikuntaa vs. iltaliikuntaa")
    nights_a = [night for night in nights if select_night_by_late_sport(night, False)]
    nights_b = [night for night in nights if select_night_by_late_sport(night, True)]
    print(describe([night.corrected_efficiency for night in nights_a]))
    print(describe([night.corrected_efficiency for night in nights_b]))
    print(ttest(nights_a, nights_b))
