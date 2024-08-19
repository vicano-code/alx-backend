#!/usr/bin/env python3
"""
Simple helper function
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """return page start and end index"""
    start_index: int = page_size * (page - 1)
    end_index: int = page_size * page

    return (start_index, end_index)
