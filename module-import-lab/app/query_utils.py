from urllib.parse import urlencode


def build_query_string(base_url: str, *, safe_mode: bool = True, **kwargs: str) -> str:
    if not kwargs:
        return base_url
    
    return f"{base_url}?{urlencode(kwargs)}"
    
