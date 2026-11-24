from datetime import date

import pytest
import requests

from ingestion import ingest


def test_save_raw_uses_partitioned_path_and_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(ingest, "RAW_DIR", tmp_path)
    payload = {"hourly": {"time": ["2026-11-19T00:00"], "pm2_5": [12.3]}}

    first = ingest.save_raw("Mumbai", payload, date(2026, 11, 19))
    second = ingest.save_raw("Mumbai", payload, date(2026, 11, 19))

    expected = tmp_path / "city=Mumbai" / "date=2026-11-19" / "data.json"
    assert first == second == expected
    assert expected.exists()
    assert len(list(tmp_path.rglob("data.json"))) == 1


def test_fetch_city_raises_on_http_error(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            raise requests.HTTPError("500 Server Error")

    monkeypatch.setattr(ingest.requests, "get", lambda *args, **kwargs: FakeResponse())

    with pytest.raises(requests.HTTPError):
        ingest.fetch_city("Mumbai", 19.0760, 72.8777)


def test_main_exits_with_code_1_when_a_city_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(ingest, "RAW_DIR", tmp_path)

    def always_fail(name, lat, lon):
        raise requests.exceptions.ConnectionError("network down")

    monkeypatch.setattr(ingest, "fetch_city", always_fail)

    with pytest.raises(SystemExit) as excinfo:
        ingest.main()

    assert excinfo.value.code == 1