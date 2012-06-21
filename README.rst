What is this?
=============

This package allows Ella users to change default behavior of category listing
pages. By default, each page has same number of objects (if there is enough
of them).

Sometimes, this does not meet the site's requirements. Very often, it is
demanded, that first page should be somehow different, e.g. list one more
article that is rendered in different style (like leading article). This
is unfortunately not available with default Ella.

How to use this
===============

Setup is quite straightforward. First, install the package using pip or setuptools::

    pip install ella-listingex

Add the app to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'ella_listingex',
        ...
    )

Configure the ``ella_listingex`` to meet your requirements. Internally, this
app works by using Ella's ``CUSTOM_VIEWS`` override. This means that we
are telling Ella to use our views instead of in-built ones. ``ella_listingex``
application redefines Ella's ``ListContentType`` view to provide additional
functionality. Therefore, we need to allow ``CUSTOM_VIEWS`` and set
the ``VIEWS`` variable to the path of ``ella_listingex.views`` as shown
below::

    # Use custom views to support different number of items on the first and
    # next pages of category listings.
    CUSTOM_VIEWS = True
    VIEWS = 'ella_listingex.views'

Next step is to set the pagination::

    LISTINGEX_PAGINATE_BY = 10        # Default number of objects per page
    LISTINGEX_FIRST_PAGE_COUNT = 11   # Number of objects on first page

The ``ella_listingex`` works on all category listings which are not blacklisted.
If you need tu turn the special behaviour off on some pages, use the
``LISTINGEX_BLACKLIST`` configuration option to provide list of regular
expressions which will be matched against category's ``tree_path`` attribute.
If there is a match, the first page will be paginated normally::

    LISTINGEX_BLACKLIST = (           # Blacklist categories, whose tree_path
        r'^blogs',                    # matches '^blogs'
    )
