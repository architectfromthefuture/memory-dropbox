from hashlib import sha256

from memory_dropbox.config import settings


def embed_text(text: str) -> list[float]:
    # Deterministic local embedding stub keeps MVP self-contained.
    digest = sha256(text.encode("utf-8")).digest()
    dim = settings.embedding_dim
    values = []
    for i in range(dim):
        b = digest[i % len(digest)]
        values.append((b / 255.0) * 2 - 1)
    return values

