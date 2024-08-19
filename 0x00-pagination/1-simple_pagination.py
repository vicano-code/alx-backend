#!/usr/bin/env python3
"""
Simple pagination
"""
import csv
import math
from typing import List, Tuple


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        # Validate input type and value
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        # get index range of page
        idx_range: Tuple = index_range(page, page_size)

        return self.dataset()[idx_range[0]:idx_range[1]]


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """return page start and end index"""
    start_index: int = page_size * (page - 1)
    end_index: int = page_size * page

    return (start_index, end_index)
