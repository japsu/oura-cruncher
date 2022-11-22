from .night import Night
from .sheets import put_nights_data


def main():
    nights = list(Night.get_nights_from_oura())
    put_nights_data(nights)

    nights = Night.get_nights_from_sheets()
    for night in nights:
        print(night)


if __name__ == "__main__":
    main()
