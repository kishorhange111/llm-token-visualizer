"""Shared test fixtures: a tiny fake tokenizer, so no test downloads anything."""

from types import SimpleNamespace

import pytest


class WordTokenizer:
    """Stand-in for a Hugging Face tokenizer: splits on spaces and wraps in [CLS] ... [SEP].

    Mimics the two calls the app makes: tokenizer(text).input_ids and decode(id).
    """

    def __init__(self):
        self.vocab = {"[CLS]": 0, "[SEP]": 1}

    def __call__(self, text):
        """Encode text, adding new words to the vocabulary as they appear."""
        words = ["[CLS]", *text.split(), "[SEP]"]
        ids = [self.vocab.setdefault(w, len(self.vocab)) for w in words]
        return SimpleNamespace(input_ids=ids)

    def decode(self, token_id):
        """Map one id back to its word."""
        return {i: w for w, i in self.vocab.items()}[token_id]


@pytest.fixture
def tokenizer():
    """A fresh fake tokenizer."""
    return WordTokenizer()
