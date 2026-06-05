from helius.models.accounts import TMultipleAccountsModel
from helius.models.block import TBlocksModel
from helius.models.error import ErrorModel
from helius.models.systemInfo import VersionModel
from helius.models.transactions import TSignatureStatusesModel


def test_error_model_defaults():
    e = ErrorModel(code=-32000, message="oops")
    assert e.code == -32000 and e.message == "oops" and e.data is None


def test_error_model_with_data():
    e = ErrorModel(code=1, message="m", data={"k": "v"})
    assert e.data == {"k": "v"}


def test_tblocks_model():
    assert TBlocksModel.validate_python([1, 2, 3]) == [1, 2, 3]


def test_tmultiple_accounts_allows_none():
    res = TMultipleAccountsModel.validate_python(
        [
            None,
            {
                "lamports": 1,
                "owner": "o",
                "data": ["d", "b"],
                "executable": False,
                "rentEpoch": 0,
                "space": 1,
            },
        ]
    )
    assert res[0] is None and res[1].lamports == 1


def test_version_model_alias():
    v = VersionModel(**{"solana-core": "1.18.22", "feature-set": 999})
    assert v.solanaCore == "1.18.22" and v.featureSet == 999


def test_signature_statuses_allows_none():
    res = TSignatureStatusesModel.validate_python(
        [
            None,
            {"slot": 1, "confirmations": None, "err": None, "confirmationStatus": "finalized"},
        ]
    )
    assert res[0] is None and res[1].slot == 1
