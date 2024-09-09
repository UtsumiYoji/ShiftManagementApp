from django.views import generic

# Create your views here.
class TopPageView(generic.TemplateView):
    template_name = 'common/top_page.html'