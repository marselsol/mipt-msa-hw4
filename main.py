from converters import UsdRubConverter, UsdEurConverter, UsdGbpConverter, UsdCnyConverter


def main():
    amount = float(input('Введите значение в USD: \n'))

    converters = [
        UsdRubConverter(),
        UsdEurConverter(),
        UsdGbpConverter(),
        UsdCnyConverter()
    ]

    for converter in converters:
        result = converter.convert(amount)
        print(f"{amount} USD to {converter.target_currency}: {result:.2f}")


if __name__ == "__main__":
    main()