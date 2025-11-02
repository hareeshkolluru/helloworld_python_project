"""Tests for configuration"""

from src.config import Settings, get_settings


def test_settings_defaults() -> None:
    """Test that settings have appropriate defaults."""
    settings = Settings()
    assert settings.app_name == "HelloWorld FastAPI"
    assert settings.app_version == "0.1.0"
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000
    assert settings.api_v1_prefix == "/api/v1"


def test_get_settings_caching() -> None:
    """Test that get_settings returns cached instance."""
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2
