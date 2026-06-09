from typing import Optional

from .client import BinanceClient, BinanceClientError
from .logging_config import setup_logger
from .validators import (
    ValidationError,
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)

logger = setup_logger("orders")


def print_order_summary(symbol, side, order_type, quantity, price=None):
    print("\n" + "=" * 50)
    print("        ORDER REQUEST SUMMARY")
    print("=" * 50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        label = "Stop Price" if order_type == "STOP_MARKET" else "Price"
        print(f"  {label:<11}: {price}")
    print("=" * 50)


def print_order_response(result: dict):
    print("\n" + "-" * 50)
    print("        ORDER RESPONSE")
    print("-" * 50)
    print(f"  Order ID   : {result.get('orderId', 'N/A')}")
    print(f"  Symbol     : {result.get('symbol', 'N/A')}")
    print(f"  Status     : {result.get('status', 'N/A')}")
    print(f"  Side       : {result.get('side', 'N/A')}")
    print(f"  Type       : {result.get('type', 'N/A')}")
    print(f"  Quantity   : {result.get('origQty', 'N/A')}")
    print(f"  Exec. Qty  : {result.get('executedQty', 'N/A')}")
    avg_price = result.get('avgPrice') or result.get('price', 'N/A')
    print(f"  Avg Price  : {avg_price}")
    print("-" * 50)


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
):
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        qty = validate_quantity(quantity)
        validated_price = validate_price(price, order_type)

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        print(f"\n❌ Validation Error: {e}")
        return

    print_order_summary(symbol, side, order_type, qty, validated_price)

    try:
        if order_type == "STOP_MARKET":
            result = client.place_order(
                symbol=symbol, side=side, order_type=order_type,
                quantity=qty, stop_price=validated_price
            )
        else:
            result = client.place_order(
                symbol=symbol, side=side, order_type=order_type,
                quantity=qty, price=validated_price
            )

        print_order_response(result)
        print(f"\n✅ Order placed successfully! Order ID: {result.get('orderId')}\n")
        logger.info(f"Order placed successfully. orderId={result.get('orderId')}")

    except BinanceClientError as e:
        logger.error(f"API error: {e}")
        print(f"\n❌ API Error [{e.code}]: {e.message}\n")

    except Exception as e:
        logger.exception(f"Unexpected error placing order: {e}")
        print(f"\n❌ Unexpected error: {e}\n")
