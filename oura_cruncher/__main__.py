from .night import Night


def main():
    for night in Night.get_nights():
        print(night)


if __name__ == "__main__":
    main()
