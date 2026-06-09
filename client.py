import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from .logging_config import setup_logger

BASE_URL = "https://testnet.binancefuture.com"
logger = setup_logger("client")


class BinanceClientError(Exception):
    """Raised when Binance API returns an error response."""
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Binance API Error {code}: {message}")


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    def _sign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params["timestamp"] = int(time.time() * 1000)
        query = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def _handle_response(self, response: requests.Response) -> Dict:
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        try:
            data = response.json()
        except Exception:
            raise BinanceClientError(-1, f"Non-JSON response: {response.text}")
        if isinstance(data, dict) and "code" in data and data["code"] != 200:
            raise BinanceClientError(data["code"], data.get("msg", "Unknown error"))
        return data

    def get_account(self) -> Dict:
        """Fetch futures account info (connection test)."""
        params = self._sign({})
        logger.debug(f"GET /fapi/v2/account params: {params}")
        resp = self.session.get(f"{BASE_URL}/fapi/v2/account", params=params)
        return self._handle_response(resp)

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        time_in_force: str = "GTC",
    ) -> Dict:
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = time_in_force

        if order_type == "STOP_MARKET":
            params["stopPrice"] = stop_price

        logger.info(f"Placing order | Request: {params}")
        signed = self._sign(params)

        try:
            resp = self.session.post(f"{BASE_URL}/fapi/v1/order", data=signed)
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network failure: {e}")
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timed out: {e}")
            raise

        result = self._handle_response(resp)
        logger.info(f"Order response: {result}")
        return result
