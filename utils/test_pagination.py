from unittest import TestCase
from utils.pagination import make_pagination_range, make_pagination


class PaginationTest(TestCase):
    def test_make_pagination_range(self):
        # tests if the function make_pagination_range()
        # returns a pagination range
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_quantity=4,
            current_page=1,

        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_pagination_range_at_start_is_static(self):
        # tests if the pagination range remains static
        # if the number of the current page is less
        # than the middle of the range

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_quantity=4,
            current_page=1,

        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_quantity=4,
            current_page=2,

        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_quantity=4,
            current_page=3,

        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_quantity=4,
            current_page=4,

        )['pagination']
        self.assertEqual([3, 4, 5, 6], pagination)

    def test_pagination_middle_range_is_static(self):

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_quantity=4,
            current_page=10,

        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_quantity=4,
            current_page=12,

        )['pagination']
        self.assertEqual([11, 12, 13, 14], pagination)

    def test_pagination_range_at_end_is_static(self):

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_quantity=4,
            current_page=18,

        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_quantity=4,
            current_page=19,

        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_quantity=4,
            current_page=20,

        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
