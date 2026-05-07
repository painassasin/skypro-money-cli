import pytest

from skypro.config import settings as settings_module


@pytest.fixture
def settings_file_path(tmp_path):
    return tmp_path / 'settings.toml'


@pytest.fixture(autouse=True)
def cleanup_settings(monkeypatch):
    yield
    monkeypatch.delenv('TAX_PERCENT', raising=False)
    monkeypatch.delenv('DEFAULT_REQUEST_TIMEOUT', raising=False)
    monkeypatch.delenv('LOG_LEVEL', raising=False)
    monkeypatch.delenv('SKYPRO__EMAIL', raising=False)
    monkeypatch.delenv('SKYPRO__PASSWORD', raising=False)


def test_save_settings_writes_toml_file(settings_file_path):
    current_settings = settings_module.Settings(
        tax_percent=4.0,
        default_request_timeout=10,
        log_level='DEBUG',
        skypro=settings_module.SkyProSettings(
            email='mentor@example.com',
            password='secret-password',
        ),
    )

    settings_module.save_settings(current_settings, settings_file_path)

    assert settings_file_path.read_text(encoding='utf-8') == (
        'tax_percent = 4.0\n'
        'default_request_timeout = 10\n'
        'log_level = "DEBUG"\n\n'
        '[skypro]\n'
        'email = "mentor@example.com"\n'
        'password = "secret-password"\n'
    )


def test_ensure_settings_file_creates_default_toml(settings_file_path):
    settings_module.ensure_settings_file(settings_file_path)

    assert settings_file_path.read_text(encoding='utf-8') == (
        'tax_percent = 6.0\n'
        'default_request_timeout = 3\n'
        'log_level = "INFO"\n\n'
        '[skypro]\n'
        'email = ""\n'
        'password = ""\n'
    )


def test_get_settings_reads_values_from_toml_file(settings_file_path, monkeypatch):
    monkeypatch.delenv('TAX_PERCENT', raising=False)
    monkeypatch.delenv('DEFAULT_REQUEST_TIMEOUT', raising=False)
    monkeypatch.delenv('LOG_LEVEL', raising=False)
    monkeypatch.delenv('SKYPRO__EMAIL', raising=False)
    monkeypatch.delenv('SKYPRO__PASSWORD', raising=False)
    settings_file_path.write_text(
        'tax_percent = 4.5\n'
        'default_request_timeout = 10\n'
        'log_level = "DEBUG"\n\n'
        '[skypro]\n'
        'email = "mentor@example.com"\n'
        'password = "secret-password"\n',
        encoding='utf-8',
    )

    current_settings = settings_module.get_settings(settings_file_path)

    assert current_settings.tax_percent == 4.5
    assert current_settings.default_request_timeout == 10
    assert current_settings.log_level == 'DEBUG'
    assert current_settings.skypro.email == 'mentor@example.com'
    assert current_settings.skypro.password == 'secret-password'
