from functools import cache

from oura.v2 import OuraClientV2

from ..config import config


@cache
def get_client():
    return OuraClientV2(personal_access_token=config.oura.token)
