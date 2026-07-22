import app.bank_utils
import app.date_utils
import app.query_utils

import pytest

@pytest.mark.parametrize(
    ("balance","amount","except_balance"),[
        (100, 50, 50),
        (100, 100, 0),
        (100, 0, 100),
    ]
)
def test_withdraw_money(balance, amount, except_balance)->None:
    assert app.bank_utils.withdraw_money(balance, amount) == except_balance



def test_reject_balance_less_than_zero()->None:
    with pytest.raises(ValueError):
        app.bank_utils.withdraw_money(100, -50)


def test_reject_amount_more_than_balance()->None:
    with pytest.raises(app.bank_utils.InsufficientFundsError):
        app.bank_utils.withdraw_money(100, 150)



@pytest.mark.parametrize(
    ("base_url","safe_mode", "kwargs","expected_query_string"),[
        ("https://google.com",True,{"search": "python", "q":"python"},"https://google.com?search=python&q=python"),
        ("https://google.com",False,{"search": "python", "q":"python"},"https://google.com?search=python&q=python"),
        ("https://google.com",True,{},"https://google.com"),
        ("https://google.com",False,{},"https://google.com"),
    ]
)
def test_build_query_string(base_url, safe_mode, kwargs, expected_query_string):
    assert app.query_utils.build_query_string(base_url, safe_mode=safe_mode, **kwargs) == expected_query_string




