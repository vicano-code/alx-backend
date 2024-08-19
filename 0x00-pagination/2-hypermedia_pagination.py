#!/usr/bin/env python3
"""
Simple pagination
"""
import csv
import math
from typing import List, Tuple, Dict, Optional


def index_range(page: int, page_size: int) -> Tuple[int, int]:
  """return page start and end index"""
  start_index = page_size * (page - 1)
  end_index = page_size * page
  return start_index, end_index


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
        idx_range = index_range(page, page_size)

        return self.dataset()[idx_range[0]:idx_range[1]]


    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """hypermedia pagination
        """

        dict = {
            "page_size": page_size if page * page_size < len(self.dataset())
                         else 0,
            "page": page,
            "data": self.get_page(page, page_size),
            "next_page": page + 1 if (page * page_size) < len(self.dataset())
                         else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": math.ceil(len(self.dataset()) / page_size)
        }
        return dict
