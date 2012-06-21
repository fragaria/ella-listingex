'''
Created on 21.6.2012

@author: xaralis
'''
import re

from datetime import date

from django.conf import settings
from django.http import Http404

from ella.core.cache import get_cached_object_or_404
from ella.core.models.main import Category
from ella.core.models.publishable import Listing
from ella.core.views import ListContentType, ObjectDetail, get_content_type

from .paginator import PaginatorEx
from .conf import listingex_settings


class ListContentTypeEx(ListContentType):
    """
    Extending standard Ella category/listing view by possibility of having
    different number of items on the first page.

    For reference on definition of pagination settings, @see: listingex.conf.
    """
    def __init__(self, *args, **kwargs):
        self.whitelist = self._compile_patterns(listingex_settings.WHITELIST)
        self.blacklist = self._compile_patterns(listingex_settings.BLACKLIST)

    def get_context(self, request, category='', year=None, month=None, \
        day=None, content_type=None,
        paginate_by=listingex_settings.PAGINATE_BY):

        # pagination
        if 'p' in request.GET and request.GET['p'].isdigit():
            page_no = int(request.GET['p'])
        else:
            page_no = 1

        # if we are not on the first page, display a different template
        category_title_page = page_no == 1

        kwa = {}
        if year:
            category_title_page = False
            year = int(year)
            kwa['publish_from__year'] = year

        if month:
            try:
                month = int(month)
                date(year, month, 1)
            except ValueError:
                raise Http404()
            kwa['publish_from__month'] = month

        if day:
            try:
                day = int(day)
                date(year, month, day)
            except ValueError:
                raise Http404()
            kwa['publish_from__day'] = day

        cat = get_cached_object_or_404(Category, tree_path=category,
                                       site__id=settings.SITE_ID)
        kwa['category'] = cat
        if category:
            kwa['children'] = Listing.objects.ALL

        if content_type:
            ct = get_content_type(content_type)
            kwa['content_types'] = [ct]
        else:
            ct = False

        qset = Listing.objects.get_queryset_wrapper(kwa)

        if self.is_ex_applied(cat):
            per_first_page = (listingex_settings.FIRST_PAGE_COUNT or
                              paginate_by)
        else:
            per_first_page = paginate_by

        paginator = PaginatorEx(qset, per_first_page, paginate_by)

        if page_no > paginator.num_pages or page_no < 1:
            raise Http404()

        page = paginator.page(page_no)
        listings = page.object_list

        context = {
                'page': page,
                'is_paginated': paginator.num_pages > 1,
                'results_per_page': paginate_by,
                'content_type': ct,
                'content_type_name': content_type,
                'listings': listings,
                'category': cat,
                'is_homepage': (not bool(category) and page_no == 1
                                and year is None),
                'is_title_page': category_title_page,
                'archive_entry_year': lambda: self._archive_entry_year(cat),
            }

        return context

    def _compile_patterns(self, pattern_list):
        patterns = []
        for patt in pattern_list:
            patterns.append(re.compile(patt))
        return patterns

    def is_ex_applied(self, category):
        """
        Test if special listing behavior is applied for this category
        based on it's tree path.
        """
        for patt in self.whitelist:
            if patt.match(category.tree_path):
                return True

        for patt in self.blacklist:
            if patt.match(category.tree_path):
                return False

        return True

home = category_detail = list_content_type = ListContentTypeEx()
object_detail = ObjectDetail()
