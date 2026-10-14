"""Tokenization and HTML rendering logic."""
import re
from pathlib import Path

from token_visualizer import COLORS, MODELS, render_tokens_html, tokenize

SPAN = re.compile(r'<span style="color: (#[0-9A-F]{6}); font-weight: bold;">(.*?)</span> ')


def test_tokenize_returns_ids_and_pieces_in_order(tokenizer):
    pieces = tokenize(tokenizer, "the cat sat")
    assert [p for _, p in pieces] == ["[CLS]", "the", "cat", "sat", "[SEP]"]
    assert [i for i, _ in pieces] == [0, 2, 3, 4, 1]


def test_special_tokens_count_towards_the_total(tokenizer):
    assert len(tokenize(tokenizer, "")) == 2  # just [CLS] and [SEP]


def test_render_one_span_per_token_in_order():
    out = render_tokens_html(["a", "b", "c"])
    assert [text for _, text in SPAN.findall(out)] == ["a", "b", "c"]
    assert SPAN.sub("", out) == ""  # nothing else in the output


def test_render_cycles_colours():
    pieces = [str(i) for i in range(len(COLORS) * 2 + 1)]
    colours = [c for c, _ in SPAN.findall(render_tokens_html(pieces))]
    assert colours == [COLORS[i % len(COLORS)] for i in range(len(pieces))]
    assert all(a != b for a, b in zip(colours, colours[1:], strict=False))  # neighbours always differ


def test_render_accepts_tokenize_output(tokenizer):
    pieces = tokenize(tokenizer, "hi there")
    assert render_tokens_html(pieces) == render_tokens_html([p for _, p in pieces])


def test_render_custom_colours():
    out = render_tokens_html(["x", "y"], colors=["#000000"])
    assert [c for c, _ in SPAN.findall(out)] == ["#000000", "#000000"]


def test_render_empty():
    assert render_tokens_html([]) == ""


def test_every_model_is_documented_in_the_readme():
    readme = (Path(__file__).resolve().parent.parent / "README.md").read_text(encoding="utf-8")
    for hub_id in MODELS.values():
        assert f"`{hub_id}`" in readme, hub_id


def test_model_ids_look_like_hub_ids():
    for hub_id in MODELS.values():
        assert re.fullmatch(r"[\w.-]+(/[\w.-]+)?", hub_id), hub_id


def test_render_escapes_html_in_token_text():
    # The app renders with unsafe_allow_html, so raw token text must never become markup.
    out = render_tokens_html(["<b>", "a&b", '"x"'])
    assert [text for _, text in SPAN.findall(out)] == ["&lt;b&gt;", "a&amp;b", "&quot;x&quot;"]
    assert "<b>" not in out
