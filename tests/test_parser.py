
import yaml
from amt2abc.parser.abc_parser import ABCParser
from amt2abc.parser.amt_parser import AMTParser
from amt2abc.parser.gs_parser import GSParser


def test_amt_parser_empty_dir(tmp_path):
    parser = AMTParser(str(tmp_path))
    result = parser.load_all()
    assert result == []


def test_amt_parser_load_one(tmp_path):
    amt_file = tmp_path / "test.yaml"
    data = {
        "id": "test-001",
        "name": "Test",
        "domain": "die_casting",
        "triplets": [
            {
                "cause": "a",
                "effect": "b",
                "relation": "increases",
                "mechanism": "m1",
            },
        ],
    }
    with open(amt_file, "w") as f:
        yaml.dump(data, f)
    parser = AMTParser(str(tmp_path))
    result = parser.load_all()
    assert len(result) == 1
    assert result[0].id == "test-001"


def test_abc_parser_empty_dir(tmp_path):
    parser = ABCParser(str(tmp_path))
    result = parser.load_all()
    assert result == []


def test_gs_parser_parse_text():
    parser = GSParser()
    gs = parser.parse_text("Reduce porosity rate")
    assert gs.text == "Reduce porosity rate"
