import inspect
import logging
import os

import pytest

from fsspec import filesystem
import fsspec.tests.abstract as abstract

from juicefs.spec import JuiceFS
from juicefs.juicefs import Client, _log_callback


class JuiceFSFixtures(abstract.AbstractFixtures):
    @pytest.fixture(scope="class")
    def fs(self):
        meta = os.getenv("JUICEFS_META", "redis://localhost")
        m = filesystem("jfs", auto_mkdir=True, name="test", meta=meta)
        return m

    @pytest.fixture
    def fs_path(self, tmpdir):
        return str(tmpdir)


class TestJuiceFSGet(abstract.AbstractGetTests, JuiceFSFixtures):
    pass


class TestJuiceFSPut(abstract.AbstractPutTests, JuiceFSFixtures):
    pass


class TestJuiceFSCopy(abstract.AbstractCopyTests, JuiceFSFixtures):
    pass


def test_client_exposes_max_downloads():
    assert inspect.signature(Client).parameters["max_downloads"].default == 200


def test_log_callback_uses_juicefs_level(caplog):
    with caplog.at_level(logging.DEBUG, logger="juicefs"):
        _log_callback(b"2026/11/19 00:00:00 juicefs[1] <WARNING>: warning")

    assert caplog.records[0].levelno == logging.WARNING
    assert caplog.records[0].message == "2026/11/19 00:00:00 juicefs[1] <WARNING>: warning"
