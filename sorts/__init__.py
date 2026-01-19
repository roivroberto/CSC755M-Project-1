from __future__ import annotations

from sorts import bubble, insertion, selection, shell
from sorts.gaps import available_variants, get_gaps

ALGORITHMS = {
    "bubble": bubble.sort,
    "insertion": insertion.sort,
    "selection": selection.sort,
    "shell": shell.sort,
}

__all__ = ["ALGORITHMS", "available_variants", "get_gaps"]
