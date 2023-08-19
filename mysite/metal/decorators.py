from django.core.paginator import Paginator


def if_paginator(self, request):
    paginator = Paginator(*self.to_padinator, orphans=5)
    page = paginator.get_page(request.GET.get('page', 1))
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = f"?page={page.previous_page_number()}"
    else:
        prev_url = ''
    if page.has_next():
        next_url = f"?page={page.next_page_number()}"
    else:
        next_url = ''
    context = {'page_object': page,
               'is_paginated': is_paginated,
               'next_url': next_url,
               'prev_url': prev_url
               }
    return context

def decorator_with_arguments(if_paginator,request,dict_dop):

    def my_decorator(func):
        def wrapped(*args, **kwargs):
            dict_dop.update(if_paginator(request))
            return func(*args, **kwargs)

        return wrapped

    return my_decorator