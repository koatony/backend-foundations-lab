from urllib.parse import urlencode

class PermissionDeniedError(Exception):
    pass


def generate_auth_url(user_id:str, role:str, *, is_admin:bool=False, **extra_params) -> str:
    if (role != "admin" and is_admin):
        raise PermissionDeniedError("非管理者無法開啟管理權限")
    
    if not extra_params:
        return f"https://auth.com/login?user={user_id}"
    else:
        return f"https://auth.com/login?user={user_id}&{urlencode(extra_params)}"