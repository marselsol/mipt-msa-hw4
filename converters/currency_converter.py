from abc import ABC, abstractmethod
import requests
import json
import time
import os
import logging

class ExchangeRateClient:
    def __init__(self, base_url="https://api.exchangerate-api.com/v4/latest/USD",
                 cache_file="exchange_rates.json", cache_expiry=3600,
                 max_retries=3, retry_delay=2):
        self.base_url = base_url
        self.cache_file = cache_file
        self.cache_expiry = cache_expiry
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_from_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    if time.time() - data['timestamp'] < self.cache_expiry:
                        return data['rates']
            except (json.JSONDecodeError, KeyError, IOError):
                self.logger.warning("Invalid or corrupted cache file")
        return None

    def _save_to_cache(self, rates):
        try:
            data = {'timestamp': time.time(), 'rates': rates}
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            self.logger.error(f"Failed to save cache: {e}")

    def get_rates(self):
        rates = self._load_from_cache()
        if rates:
            return rates

        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.base_url, timeout=10)
                response.raise_for_status()
                rates = response.json()['rates']
                self._save_to_cache(rates)
                return rates
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Attempt {attempt+1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
            except (KeyError, json.JSONDecodeError) as e:
                self.logger.error(f"Data parsing error: {e}")
                break

        self.logger.error("Failed to fetch exchange rates")
        return None

class CurrencyConverter(ABC):
    def __init__(self, target_currency, rate_client=None):
        self.target_currency = target_currency
        self.rate_client = rate_client or ExchangeRateClient()

    @abstractmethod
    def convert(self, amount):
        pass

class SimpleCurrencyConverter(CurrencyConverter):
    def convert(self, amount):
        rates = self.rate_client.get_rates()
        if rates and self.target_currency in rates:
            return amount * rates[self.target_currency]
        raise ValueError(f"Currency {self.target_currency} not found in rates")