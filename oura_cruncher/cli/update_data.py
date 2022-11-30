import click

from ..models.night import Night
from ..services.sheets import get_nights_data, put_nights_data


@click.command
def update_data():
    nights = list(Night.get_nights_from_oura())
    nights_data_from_sheets = get_nights_data()
    Night.update_nights_from_sheets(nights, nights_data_from_sheets)

    put_nights_data(nights)
