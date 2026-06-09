# Binance Futures Testnet Trading Bot

A Python CLI application to place Market, Limit, and Stop-Market orders on the **Binance Futures Testnet (USDT-M)**. Built with a clean, layered architecture, structured logging, and full error handling.

---

## Project Structure
---

## Setup

### 1. Register on Binance Futures Testnet

1. Go to https://testnet.binancefuture.com
2. Sign in with GitHub
3. Navigate to **API Key** section and generate credentials
4. Copy your **API Key** and **Secret Key**

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run

### Option A — Pass credentials as arguments

```bash
python cli.py \
  --api-key YOUR_API_KEY \
  --api-secret YOUR_API_SECRET \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

### Option B — Use environment variables (recommended)

```bash
export BINANCE_API_KEY=your_key
export BINANCE_API_SECRET=your_secret
```

Then run without credential flags:

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

---

## Usage Examples

### Place a MARKET BUY order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a LIMIT SELL order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000
```

### Place a STOP_MARKET order (bonus order type)
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --price 60000
```

---

## Logging

Logs are written to `logs/trading_bot_YYYYMMDD.log`. Each entry includes timestamps, log level, API request parameters, full API response, and errors with tracebacks.

---

## Assumptions

- All orders use Binance Futures Testnet only, never live Binance.
- LIMIT orders use timeInForce=GTC by default.
- STOP_MARKET is the bonus third order type.

---

## Requirements

- Python 3.8+
- `requests` (see requirements.txt)
