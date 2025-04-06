from .currency_converter import SimpleCurrencyConverter

class UsdGbpConverter(SimpleCurrencyConverter):
    def __init__(self, rate_client=None):
        super().__init__('GBP', rate_client)