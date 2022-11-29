from .night import Night
from .sheets import put_nights_data, get_nights_data


def main():
    nights = list(Night.get_nights_from_oura())
    nights_data_from_sheets = get_nights_data()
    Night.update_nights_from_sheets(nights, nights_data_from_sheets)

    put_nights_data(nights)

    for night in nights:
        print(night)


if __name__ == "__main__":
    main()
