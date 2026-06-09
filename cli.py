#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot — CLI Entry Point

Usage examples:
  python cli.py --api-key YOUR_KEY --api-secret YOUR_SECRET \
      --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  python cli.py --api-key YOUR_KEY --api-secret YOUR_SECRET \
      --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000

  python cli.py --api-key YOUR_KEY --api-secret YOUR_SECRET \
      --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --price 60000

Alternatively, set environment variables BINANCE_API_KEY and BINANCE_API_SECRET
to avoid passing credentials on every run.
"""

import argparse
import os
import sys

from bot.client import BinanceClient, BinanceClientError
from bot.logging_config import setup_logger
from bot.orders import place_order

logger = setup_logger("cli")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Credentials (env var fallback)
    parser.add_argument(
        "--api-key",
        default=os.environ.get("BINANCE_API_KEY"),
        help="Binance Testnet API key (or set BINANCE_API_KEY env var)",
    )
    parser.add_argument(
        "--api-secret",
        default=os.environ.get("BINANCE_API_SECRET"),
        help="Binance Testnet API secret (or set BINANCE_API_SECRET env var)",
    )

    # Order params
    parser.add_argument("--symbol",   required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",     required=True, choices=["BUY", "SELL"], help="BUY or SELL")
    parser.add_argument("--type",     required=True, dest="order_type",
                        choices=["MARKET", "LIMIT", "STOP_MARKET"],
                        help="Order type: MARKET, LIMIT, or STOP_MARKET (bonus)")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price",    default=None,
                        help="Limit price (required for LIMIT); stop price for STOP_MARKET")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.api_key or not args.api_secret:
        parser.error(
            "API credentials are required. Pass --api-key / --api-secret "
            "or set BINANCE_API_KEY / BINANCE_API_SECRET environment variables."
        )

    logger.info("Starting trading bot session")
    client = BinanceClient(api_key=args.api_key, api_secret=args.api_secret)

    # Quick connectivity check
    try:
        client.get_account()
        logger.info("Connected to Binance Futures Testnet ✓")
        print("✅ Connected to Binance Futures Testnet")
    except BinanceClientError as e:
        logger.error(f"Authentication/connection failed: {e}")
        print(f"❌ Connection failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Network error during connection check: {e}")
        print(f"❌ Network error: {e}")
        sys.exit(1)

    place_order(
        client=client,
        symbol=args.symbol,
        side=args.side,
        order_type=args.order_type,
        quantity=args.quantity,
        price=args.price,
    )

    logger.info("Session complete")


if __name__ == "__main__":
    main()
