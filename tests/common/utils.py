from random import choices
from typing import Any, Tuple


def weighted_choices(weighted_pool: Tuple[Any, int], **kwargs) -> Any:
    pool, weights = zip(*weighted_pool)
    return choices(pool, weights=weights, **kwargs)
