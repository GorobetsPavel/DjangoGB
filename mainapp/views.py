from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .models import News


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"
    paginated_by = 3

    def get_context_data(self, **kwargs):
        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(News.objects.all(), self.paginated_by)
        page = paginator.get_page(page_number)

        context = super().get_context_data(**kwargs)

        context['page'] = page

        return context


class NewsDetailPageView(TemplateView):
    template_name = ""

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['news_obj'] = get_object_or_404(News, pk=pk)

        return context


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"
