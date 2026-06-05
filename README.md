# helius-api

A lightweight [Helius](https://www.helius.dev/) RPC client in Python for Solana. It offers a clean, typed wrapper around the Helius JSON-RPC HTTP methods, grouped into intuitive modules for accounts, blocks, epochs, slots, tokens, transactions, inflation/rewards, and system information.

## Features

- Simple, ergonomic client built on top of the Helius RPC API
- Logically grouped modules accessible as properties on the client
- Typed models (via [Pydantic](https://docs.pydantic.dev/)) for structured responses
- Graceful error handling — RPC and network errors return `None` instead of raising
- Covers a broad surface of Solana RPC methods:
  - **Accounts** — account info, balances, program accounts, rent exemption, largest accounts
  - **Block** — blocks, block height/time, production, commitment, latest blockhash
  - **Epoch** — epoch info, schedule, leader schedule
  - **Slot** — current slot, slot leaders, snapshot info
  - **Token** — token balances, accounts by owner/delegate, supply, largest accounts
  - **Transactions** — transaction history, signatures, statuses, send/simulate, airdrops
  - **Inflation & Rewards** — inflation governor, rate, and reward details
  - **System Info** — health, version, identity, cluster nodes, prioritization fees, supply

## Requirements

- Python >= 3.12
- A Helius API key ([get one here](https://www.helius.dev/))

## Installation

Install using pip:

```shell
pip install helius-api
```
**Requirements:** Python 3.7+
___


## Quick Start

```python
from helius import Helius

# Initialize the client with your Helius API key
client = Helius(apiKey="YOUR_API_KEY")

# Get the SOL balance (in lamports) for an account
balance = client.accounts.getBalance("So11111111111111111111111111111111111111112")
print(balance)

# Get account info
info = client.accounts.getInfo("So11111111111111111111111111111111111111112")
print(info)

# Check cluster health
print(client.systemInfo.getHealth())

# Get the supply of a token mint
supply = client.token.getTokenSupply("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
print(supply)
```

## Configuration

The `Helius` client accepts the following constructor arguments:

| Argument  | Type           | Default                              | Description                          |
|-----------|----------------|--------------------------------------|--------------------------------------|
| `apiKey`  | `str`          | _required_                           | Your Helius API key                  |
| `jsonrpc` | `str \| None`  | `"2.0"`                              | JSON-RPC version                     |
| `id`      | `int \| None`  | `1`                                  | JSON-RPC request ID                  |
| `url`     | `str \| None`  | `https://mainnet.helius-rpc.com`     | Base RPC URL                         |

## Modules

The client exposes the following modules as properties:

| Property                  | Description                                                        |
|---------------------------|--------------------------------------------------------------------|
| `client.accounts`         | Account info, balances, program accounts, rent exemption           |
| `client.block`            | Blocks, heights, production, commitment, blockhashes               |
| `client.epoch`            | Epoch info, schedules, leader schedules                            |
| `client.slot`             | Current slots, leaders, snapshot info                              |
| `client.token`            | Token balances, accounts by owner/delegate, supply                 |
| `client.transactions`     | Transaction history, signatures, statuses, send/simulate, airdrops |
| `client.inflationRewards` | Inflation governor, rate, and reward details                       |
| `client.systemInfo`       | Health, version, identity, cluster nodes, prioritization fees      |

## Error Handling

Methods return `None` when a request fails — either due to a network error or an
RPC-level error. Error details are printed to the console, so always check for
`None` before using a result:

```python
result = client.accounts.getBalance("invalid-key")
if result is None:
    print("Request failed")
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## License

Released under the [MIT License](LICENSE-MIT).
