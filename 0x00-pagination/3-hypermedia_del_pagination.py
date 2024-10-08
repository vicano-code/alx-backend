#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination

The goal here is that if between two queries, certain rows are removed from
the dataset, the user does not miss items from dataset when changing page.
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """return dictionary of page properties"""
        # validate index range
        data_len = len(self.indexed_dataset())
        assert index < data_len

        start_index = max(0, index)  # Ensure index is non-negative
        end_index = min(start_index + page_size, data_len)
        data_list = []
        idx = start_index
        while idx < end_index:
            if idx in self.indexed_dataset().keys():
                data_list.append((idx, self.indexed_dataset()[idx]))
            idx += 1

        data = dict(data_list)

        return {
            "index": start_index,
            "next_index": end_index if end_index < data_len else None,
            "page_size": len(data),
            "data": data
        }
