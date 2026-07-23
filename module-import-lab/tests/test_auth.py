import app.auth_utils
import pytest

def test_user_admin_permissionError():
    with pytest.raises(app.auth_utils.PermissionDeniedError):
        s = app.auth_utils.generate_auth_url('a','user', is_admin = True)

@pytest.mark.parametrize(
    ('user_id', 'role', 'expected_url'),[
        ("123", "user", "https://auth.com/login?user=123")
    ]
)
def test_no_extra_parameters(user_id, role, expected_url):
    assert app.auth_utils.generate_auth_url(user_id, role) == expected_url



@pytest.mark.parametrize(
    ('user_id', 'role', 'extra_params', 'expected_url'),[
        ("123", "user", {"theme":"dark", "lang":"zh_TW"}, "https://auth.com/login?user=123&theme=dark&lang=zh_TW")
    ]
)
def test_extra_parameters(user_id, role, extra_params, expected_url)->None:
    assert app.auth_utils.generate_auth_url(user_id, role, **extra_params) == expected_url