from rest_framework.pagination import PageNumberPagination

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Студенты", 'url_name': 'students'},
        {'title': "Преподователи", 'url_name': 'teachers'},
        {'title': "Журнал", 'url_name': 'gradebook'}
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context


class StudentAPIPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5
