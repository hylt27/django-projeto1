import math
from django.core.paginator import Paginator


def make_pagination_range(page_range, page_quantity, current_page):
    '''
    page_range: is a list of the pages

    page_quantity: is the number of pages we want to show in the pagination

    current_page: is the number of the page that the user is accessing

    '''
    half_of_range = math.ceil(page_quantity/2)
    range_start = current_page - half_of_range
    range_stop = current_page + half_of_range
    total_pages = len(page_range)

    '''
    half_of_range: is half of the number of pages we want to show in the
    pagination range

    range_start: is the first number that appears in the pagination range
    [1 2 3 4]
     ^

    range_stop: is the last number that appears in the pagination range
    [1 2 3 4]
           ^
    total_pages: is the total number of pages
    '''

    range_start_offset = abs(range_start) if range_start < 0 else 0

    if range_start < 0:
        range_start = 0
        range_stop += range_start_offset
    
    if range_stop >= total_pages:
        range_start = range_start - abs(total_pages - range_stop)
        
    pagination = page_range[range_start:range_stop]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'page_quantity': page_quantity,
        'current_page': current_page,
        'total_pages': total_pages,
        'range_start': range_start,
        'range_stop': range_stop,
        'first_page_out_of_range': current_page > half_of_range,
        'last_page_out_of_range': range_stop < total_pages,
    }


def make_pagination(request, queryset, per_page, page_quantity=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        page_range=paginator.page_range,
        page_quantity=page_quantity,
        current_page=current_page,
    )

    return page_obj, pagination_range