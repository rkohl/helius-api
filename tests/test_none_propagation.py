from unittest.mock import MagicMock

import pytest


@pytest.mark.parametrize(
    "call",
    [
        lambda c: c.accounts.getAccountInfo("P"),
        lambda c: c.accounts.getBalance("P"),
        lambda c: c.accounts.getLargestAccounts(),
        lambda c: c.block.getBlock(1),
        lambda c: c.block.getBlockHeight(),
        lambda c: c.epoch.getEpochInfo(),
        lambda c: c.inflationRewards.getInflationRate(),
        lambda c: c.slot.getSlot(),
        lambda c: c.systemInfo.getHealth(),
        lambda c: c.systemInfo.getSupply(),
        lambda c: c.token.getTokenSupply("M"),
        lambda c: c.transactions.getTransactionCount(),
        lambda c: c.transactions.simulateTransaction("T"),
    ],
)
def test_returns_none_when_request_fails(client, call):
    client._makeRequest = MagicMock(return_value=None)
    assert call(client) is None
