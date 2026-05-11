from unittest.mock import call

import pytest
from pydantic import SecretStr

import skypro.config.settings as settings_module
from skypro.config.service import (
    configure_skypro_settings,
    ensure_skypro_configured,
    is_skypro_configured,
)
from skypro.config.settings import Settings, SkyProSettings, save_settings


@pytest.fixture
def mocked_get_settings(mocker):
    return mocker.patch('skypro.config.service.get_settings')


@pytest.fixture
def mocked_save_settings(mocker):
    return mocker.patch('skypro.config.service.save_settings')


@pytest.fixture
def mocked_configure_skypro_settings(mocker):
    return mocker.patch('skypro.config.service.configure_skypro_settings')


def test_is_skypro_configured_returns_true_for_complete_section():
    settings = build_settings(
        skypro=SkyProSettings(
            email='mentor@example.com', password=SecretStr('secret-password')
        )
    )

    assert is_skypro_configured(settings)


def test_is_skypro_configured_returns_false_for_incomplete_section():
    settings = build_settings(skypro=SkyProSettings(email='mentor@example.com'))
    assert not is_skypro_configured(settings)


def test_configure_skypro_settings_updates_only_skypro_section(
    console, mocked_get_settings, mocked_save_settings
):
    settings = build_settings(
        tax_percent=13.0,
        skypro=SkyProSettings(
            email='old@example.com', password=SecretStr('old-password')
        ),
    )
    mocked_get_settings.return_value = settings
    console.input.side_effect = ['new@example.com', 'new-password']

    updated_settings = configure_skypro_settings(console)

    mocked_get_settings.assert_called_once_with()
    console.input.assert_has_calls(
        [call('Email [old@example.com]: '), call('Password: ', password=True)]
    )
    mocked_save_settings.assert_called_once_with(updated_settings)
    assert updated_settings.tax_percent == 13.0
    assert updated_settings.skypro.email == 'new@example.com'
    assert updated_settings.skypro.password.get_secret_value() == 'new-password'


@pytest.mark.usefixtures('mocked_save_settings')
def test_configure_skypro_settings_preserves_current_password_on_blank_input(
    console, mocked_get_settings
):
    settings = build_settings(
        skypro=SkyProSettings(
            email='mentor@example.com', password=SecretStr('saved-password')
        )
    )
    mocked_get_settings.return_value = settings
    console.input.side_effect = ['', '']

    updated_settings = configure_skypro_settings(console)

    assert updated_settings.skypro.email == 'mentor@example.com'
    assert updated_settings.skypro.password.get_secret_value() == 'saved-password'


def test_ensure_skypro_configured_returns_existing_settings(
    console, mocked_get_settings, mocked_configure_skypro_settings
) -> None:
    settings = build_settings(
        skypro=SkyProSettings(
            email='mentor@example.com', password=SecretStr('secret-password')
        )
    )
    mocked_get_settings.return_value = settings

    actual_settings = ensure_skypro_configured(console)

    mocked_get_settings.assert_called_once_with()
    mocked_configure_skypro_settings.assert_not_called()
    assert actual_settings == settings


def test_ensure_skypro_configured_runs_wizard_for_missing_credentials(
    console, mocked_get_settings, mocked_configure_skypro_settings
) -> None:
    incomplete_settings = build_settings()
    mocked_get_settings.return_value = incomplete_settings
    configured_settings = build_settings(
        skypro=SkyProSettings(
            email='mentor@example.com', password=SecretStr('secret-password')
        )
    )
    mocked_configure_skypro_settings.return_value = configured_settings

    actual_settings = ensure_skypro_configured(console)

    mocked_configure_skypro_settings.assert_called_once_with(console)
    assert actual_settings == configured_settings


def test_save_settings_persists_secret_password_as_plain_string() -> None:
    settings = build_settings(
        skypro=SkyProSettings(
            email='mentor@example.com', password=SecretStr('secret-password')
        )
    )

    save_settings(settings)

    saved = settings_module.SETTINGS_FILE_PATH.read_text(encoding='utf-8')
    assert '"password": "secret-password"' in saved


def build_settings(
    *,
    tax_percent: float = 6.0,
    default_request_timeout: int = 3,
    skypro: SkyProSettings | None = None,
) -> Settings:
    return Settings.model_construct(
        tax_percent=tax_percent,
        default_request_timeout=default_request_timeout,
        skypro=skypro or SkyProSettings(),
    )
