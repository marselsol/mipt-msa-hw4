from .currency_converter import SimpleCurrencyConverter

class UsdRubConverter(SimpleCurrencyConverter):
    def __init__(self, rate_client=None):
        super().__init__('RUB', rate_client)