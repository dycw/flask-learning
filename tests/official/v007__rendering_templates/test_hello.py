from __future__ import annotations

from markupsafe import Markup


def test_hello() -> None:
    assert Markup(
        "<strong>Hello %s!</strong>",
    ) % "<blink>hacker</blink>" == Markup(
        "<strong>Hello &lt;blink&gt;hacker&lt;/blink&gt;!</strong>",
    )
    assert Markup.escape("<blink>hacker</blink>") == Markup(
        "&lt;blink&gt;hacker&lt;/blink&gt;",
    )
    assert (
        Markup("<em>Marked up</em> &raquo; HTML").striptags()
        == "Marked up \xbb HTML"
    )
