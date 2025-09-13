from django.shortcuts import render
from django.views import View

class EULAView(View):
    template = 'accounts/eula.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template)