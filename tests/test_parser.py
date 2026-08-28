import pytest
import yaml
from amt2abc.models.amt import AMT
from amt2abc.parser.abc_parser import ABCParser
from amt2abc.parser.amt_parser import AMTParseError, AMTParser
from amt2abc.parser.gs_parser import GSParser
from pydantic import ValidationError


def _valid_amt_dict():
    return {
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


def test_amt_parser_empty_dir(tmp_path):
    parser = AMTParser(str(tmp_path))
    result = parser.load_all()
    assert result == []


def test_amt_parser_load_one(tmp_path):
    amt_file = tmp_path / "test.yaml"
    with amt_file.open("w") as f:
        yaml.dump(_valid_amt_dict(), f)
    parser = AMTParser(str(tmp_path))
    result = parser.load_all()
    assert len(result) == 1
    assert result[0].id == "test-001"


def test_amt_parser_load_text():
    parser = AMTParser()
    amt = parser.load_text(yaml.safe_dump(_valid_amt_dict()))
    assert isinstance(amt, AMT)
    assert amt.domain == "die_casting"


def test_amt_parser_invalid_yaml_raises():
    parser = AMTParser()
    with pytest.raises(AMTParseError):
        parser.load_text("not: [valid: yaml")


def test_amt_parser_non_mapping_raises():
    parser = AMTParser()
    with pytest.raises(AMTParseError):
        parser.load_text("- just\n- a\n- list")


def test_amt_parser_invalid_model_raises():
    parser = AMTParser()
    bad = dict(_valid_amt_dict())
    bad["triplets"] = [{"cause": "only_cause"}]
    with pytest.raises(AMTParseError):
        parser.load_text(yaml.safe_dump(bad))


def test_amt_parser_invalid_model_relaxed(tmp_path):
    bad = dict(_valid_amt_dict())
    bad["triplets"] = [{"cause": "only_cause"}]
    bad_file = tmp_path / "bad.yaml"
    with bad_file.open("w") as f:
        yaml.dump(bad, f)
    parser = AMTParser(str(tmp_path), strict=False)
    with pytest.raises(ValidationError):
        parser.load_all()


def test_abc_parser_empty_dir(tmp_path):
    parser = ABCParser(str(tmp_path))
    result = parser.load_all()
    assert result == []


def test_gs_parser_parse_text():
    parser = GSParser()
    gs = parser.parse_text("Reduce porosity rate")
    assert gs.text == "Reduce porosity rate"
