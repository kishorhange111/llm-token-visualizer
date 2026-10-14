"""End-to-end smoke tests of the Streamlit UI, with the tokenizer download mocked out."""

from pathlib import Path

import pytest

st = pytest.importorskip("streamlit")
transformers = pytest.importorskip("transformers")
from streamlit.testing.v1 import AppTest  # noqa: E402

from .conftest import WordTokenizer  # noqa: E402

APP = str(Path(__file__).resolve().parent.parent / "app.py")


@pytest.fixture(autouse=True)
def fresh_cache():
    """load_tokenizer is cached per process; clear it so each test sees its own mock."""
    st.cache_resource.clear()
    yield
    st.cache_resource.clear()


def run_app(text, click=True):
    """Run the app, type `text`, press the button and return the AppTest."""
    at = AppTest.from_file(APP).run()
    at.text_area[0].input(text)
    if click:
        at.button[0].click()
    return at.run()


def test_shows_coloured_tokens_and_count(monkeypatch):
    loaded = []

    def fake_from_pretrained(name):
        loaded.append(name)
        return WordTokenizer()

    monkeypatch.setattr(transformers.AutoTokenizer, "from_pretrained", fake_from_pretrained)
    at = run_app("hello world")
    assert not at.exception
    assert loaded == ["bert-base-cased"]  # the first entry of the dropdown
    html = "".join(m.value for m in at.markdown)
    assert ">hello</span>" in html and ">world</span>" in html
    assert at.caption[0].value == "Token count: 4"


def test_tokenizer_failure_shows_error_instead_of_crashing(monkeypatch):
    def broken(name):
        raise OSError("offline")

    monkeypatch.setattr(transformers.AutoTokenizer, "from_pretrained", broken)
    at = run_app("hello")
    assert not at.exception
    assert "Could not load the BERT tokenizer: offline" in at.error[0].value


def test_empty_text_shows_warning(monkeypatch):
    monkeypatch.setattr(transformers.AutoTokenizer, "from_pretrained", lambda name: WordTokenizer())
    at = run_app("")
    assert "Please enter text" in at.warning[0].value
