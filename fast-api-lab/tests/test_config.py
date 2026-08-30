import os 
from app.core import Settings

def test_settings_load_from_env_file():
    settings = Settings()

    assert settings.PROJECT_NAME == "My Custom Task App"
    assert settings.DEBUG is False
    assert settings.DATABASE_URL == "sqlite:///./env_test.db"


def test_os_env_overrides_env_file(monkeypatch):
    """Test that OS env vars override .env file values"""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./override.db")
    monkeypatch.setenv("DEBUG", "true")
    
    settings = Settings()
    assert settings.DATABASE_URL == "sqlite:///./override.db"
    assert settings.DEBUG is True