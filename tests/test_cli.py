from amt2abc.cli import main
from click.testing import CliRunner


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "amt2abc" in result.output


def test_list():
    runner = CliRunner()
    result = runner.invoke(main, ["list"])
    assert result.exit_code == 0
    assert "AMT2ABC" in result.output
