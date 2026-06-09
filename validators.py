from typing import Optional


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


class ValidationError(Exception):
    pass


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s:
        raise ValidationError("Symbol cannot be empty.")
    if len(s) < 3:
        raise ValidationError(f"Invalid symbol: '{s}'. Example: BTCUSDT")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValidationError(f"Side must be one of {VALID_SIDES}, got '{side}'.")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValidationError(f"Order type must be one of {VALID_ORDER_TYPES}, got '{order_type}'.")
    return t


def validate_quantity(quantity: str) -> float:
    try:
        q = float(quantity)
    except ValueError:
        raise ValidationError(f"Quantity must be a number, got '{quantity}'.")
    if q <= 0:
        raise ValidationError("Quantity must be greater than 0.")
    return q


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        try:
            p = float(price)
        except ValueError:
            raise ValidationError(f"Price must be a number, got '{price}'.")
        if p <= 0:
            raise ValidationError("Price must be greater than 0.")
        return p
    if order_type == "STOP_MARKET":
        if price is None:
            raise ValidationError("Stop price is required for STOP_MARKET orders.")
        try:
            p = float(price)
        except ValueError:
            raise ValidationError(f"Stop price must be a number, got '{price}'.")
        if p <= 0:
            raise ValidationError("Stop price must be greater than 0.")
        return p
    return None
