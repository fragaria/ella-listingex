'''
Created on 21.6.2012

@author: xaralis
'''
from math import ceil

from django.core.paginator import Paginator, Page


class PaginatorEx(Paginator):
    """
    Extending standard django paginator by possibility of having different
    number of items on the first page.
    """
    def __init__(self, object_list, per_first_page, per_page, orphans=0,
                 allow_empty_first_page=True):
        self.object_list = object_list
        self.per_first_page = per_first_page
        self.per_page = per_page
        self.orphans = orphans
        self.allow_empty_first_page = allow_empty_first_page
        self._num_pages = self._count = None

    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        bottom = (number - 2) * self.per_page + self.per_first_page if number > 1 else 0
        top = bottom + (self.per_first_page if number == 1 else self.per_page)
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.object_list[bottom:top], number, self)

    def _get_num_pages(self):
        "Returns the total number of pages."
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            else:
                hits = max(1, self.count - self.per_first_page - self.orphans)
                self._num_pages = int(ceil(hits / float(self.per_page))) + 1 if \
                    self.count > self.per_first_page else 1
        return self._num_pages
    num_pages = property(_get_num_pages)
