from typing import TYPE_CHECKING

import pydantic
from scipy.stats import ttest_ind

if TYPE_CHECKING:
    from ..models.night import Night


def ttest(nights_a: list["Night"], nights_b: list["Night"]):
    eff_a = [night.corrected_efficiency for night in nights_a]
    eff_b = [night.corrected_efficiency for night in nights_b]

    return ttest_ind(eff_a, eff_b)
