from .currency_converter import SimpleCurrencyConverter

class UsdCnyConverter(SimpleCurrencyConverter):
    def __init__(self, rate_client=None):
        super().__init__('CNY', rate_client)