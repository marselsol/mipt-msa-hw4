from .currency_converter import SimpleCurrencyConverter

class UsdEurConverter(SimpleCurrencyConverter):
    def __init__(self, rate_client=None):
        super().__init__('EUR', rate_client)