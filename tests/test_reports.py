from src.services.report_service import save_json


def test_save_json(tmp_path):
    test_file = tmp_path / "test.json"
    save_json({"hello": "world"}, str(test_file))
    assert test_file.exists()
