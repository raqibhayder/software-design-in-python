import os
from http import HTTPStatus

from server.mock_handler import MockRequestHandler


class CombinedHandler(MockRequestHandler, ApplicationRequestHandler):
    pass


def test_nonexistent_path():
    handler = CombinedHandler("/nonexistent.txt")
    handler.do_GET()
    assert handler.status == int(HTTPStatus.NOT_FOUND)
    assert "Content-Type" in handler.headers
    assert "Content-Length" in handler.headers


def test_existing_path():
    content_str = "actual"
    content_bytes = bytes(content_str, "utf-8")

    with open("actual.txt", "wb") as byte_file_writer:
        byte_file_writer(content_bytes)

    handler = CombinedHandler("/actual.txt")
    handler.do_GET()

    assert handler.status == int(HTTPStatus.OK)
    assert handler.headers["Content-Type"] == ["text/html; charset=utf-8"]
    assert handler.headers["Content-Length"] == [str(len(content_bytes))]
    assert handler.wfile.getvalue() == content_bytes
