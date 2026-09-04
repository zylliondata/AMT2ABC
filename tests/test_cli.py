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
    assert "AMTs:" in result.output


def test_info_existing():
    runner = CliRunner()
    result = runner.invoke(main, ["info", "AMT_DC_THERMO_002"])
    assert result.exit_code == 0
    assert "AMT_DC_THERMO_002" in result.output
    assert "Triplets" in result.output


def test_info_json():
    runner = CliRunner()
    result = runner.invoke(
        main, ["info", "AMT_DC_THERMO_002", "--format", "json"]
    )
    assert result.exit_code == 0
    assert '"id": "AMT_DC_THERMO_002"' in result.output


def test_info_missing():
    runner = CliRunner()
    result = runner.invoke(main, ["info", "DOES_NOT_EXIST"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_graph_path():
    runner = CliRunner()
    result = runner.invoke(main, ["graph", "mold_temperature", "porosity_rate"])
    assert result.exit_code == 0
    assert "Path:" in result.output


def test_graph_no_path():
    runner = CliRunner()
    result = runner.invoke(main, ["graph", "xyz_unknown", "porosity_rate"])
    assert result.exit_code == 0
    assert "No path" in result.output


def test_compile():
    runner = CliRunner()
    result = runner.invoke(main, ["compile", "reduce porosity"])
    assert result.exit_code == 0
    assert "Goal:" in result.output
    assert "Matched AMTs" in result.output
