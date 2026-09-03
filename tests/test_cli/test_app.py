from typer.testing import CliRunner

from skypro.cli.app import app

runner = CliRunner()


def test_summary_ensures_skypro_configuration_before_execution(mocker) -> None:
    mocker.patch('skypro.cli.app.is_skypro_configured', return_value=True)
    mocked_show_summary = mocker.Mock(return_value='summary-task')
    mocker.patch('skypro.cli.app.commands.show_summary', new=mocked_show_summary)
    mocked_asyncio_run = mocker.patch('skypro.cli.app.asyncio.run')

    result = runner.invoke(app, ['summary'])

    assert result.exit_code == 0
    mocked_show_summary.assert_called_once()
    mocked_asyncio_run.assert_called_once()


def test_summary_fails_when_skypro_configuration_is_missing(mocker) -> None:
    mocked_console = mocker.patch('skypro.cli.app.console')
    mocker.patch('skypro.cli.app.is_skypro_configured', return_value=False)
    mocked_show_summary = mocker.patch('skypro.cli.app.commands.show_summary')
    mocked_asyncio_run = mocker.patch('skypro.cli.app.asyncio.run')

    result = runner.invoke(app, ['summary'])

    assert result.exit_code == 1
    mocked_console.print.assert_called_once_with(
        '[red]Настройки SkyPro не заданы. '
        'Укажите их командой `sky-cli config --skypro`.[/]'
    )
    mocked_show_summary.assert_not_called()
    mocked_asyncio_run.assert_not_called()


def test_config_command_prints_current_settings(mocker) -> None:
    mocked_console = mocker.patch('skypro.cli.app.console')
    mocked_configure = mocker.patch('skypro.cli.app.configure_skypro_settings')

    result = runner.invoke(app, ['config'])

    assert result.exit_code == 0
    mocked_configure.assert_not_called()
    mocked_console.print.assert_called_once_with(
        '{\n'
        '  "tax_percent": 6.0,\n'
        '  "default_request_timeout": 3,\n'
        '  "log_level": "info",\n'
        '  "skypro": {\n'
        '    "email": "mentor@example.com",\n'
        '    "password": "**********",\n'
        '    "tz": "Europe/Moscow"\n'
        '  }\n'
        '}'
    )


def test_config_command_runs_skypro_reconfiguration_with_flag(mocker) -> None:
    mocked_configure = mocker.patch('skypro.cli.app.configure_skypro_settings')

    result = runner.invoke(app, ['config', '--skypro'])

    assert result.exit_code == 0
    mocked_configure.assert_called_once()
