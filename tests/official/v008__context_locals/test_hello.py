from __future__ import annotations

from os import environ

from flask import request
from pytest import mark

from flask_learning.official.v008__context_locals.hello import app


def test_hello_1() -> None:
    with app.test_request_context("/hello", method="POST"):
        # now you can do something with the request until the
        # end of the with block, such as basic assertions:
        assert request.path == "/hello"
        assert request.method == "POST"


@mark.xfail(reason="What is 'environ'?")  # type: ignore
def test_hello_2() -> None:
    with app.request_context(environ):
        assert request.method == "POST"
