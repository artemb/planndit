from django.views.generic import View


class View(View):
    def page_render(self, request):
        title = "Planndit" #todo Сделать что-то с заголовком