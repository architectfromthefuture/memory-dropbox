"""Deterministic local embedding stub."""

from memory_dropbox.config import settings
from memory_dropbox.vector.embeddings import embed_text


def test_embed_text_is_deterministic() -> None:
    a = embed_text("hello")
    b = embed_text("hello")
    assert a == b
    assert len(a) > 0


def test_embedding_vector_length_matches_config() -> None:
    vec = embed_text("probe text")
    assert len(vec) == settings.embedding_dim
