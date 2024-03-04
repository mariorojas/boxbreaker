from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, FormView
from django.views.generic.edit import FormMixin

from .forms import AttemptForm, GameForm
from .models import Game
from .schemas import AttemptSchema


class GameDetailView(FormMixin, DetailView):
    model = Game
    form_class = AttemptForm
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'games/game_detail.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schema = AttemptSchema(many=True)
        attempts = self.object.attempts.all()
        formatted_attempts = [schema.loads(el.result) for el in attempts]
        context.update({
            'formatted_attempts': formatted_attempts,
            'remaining_attempts': settings.ATTEMPTS_LIMIT - len(formatted_attempts)
        })
        return context


class GameFormView(FormView):
    form_class = GameForm
    template_name = 'games/game_form.html'

    def form_valid(self, form):
        user = self.request.user if self.request.user.is_authenticated else None
        ip_address = self.request.META.get('REMOTE_ADDR')
        instance = form.save(owner=user, ip_address=ip_address)
        return redirect(instance.get_absolute_url())


class AttemptCreateView(CreateView):
    form_class = AttemptForm
    template_name = 'games/attempt_form.html'
    http_method_names = ['post']
    parent = None

    def post(self, request, *args, **kwargs):
        uuid = self.kwargs.get('uuid')
        self.parent = get_object_or_404(Game, uuid=uuid, completed=False)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.parent = self.parent
        return super().form_valid(form)

    def get_success_url(self):
        return self.parent.get_absolute_url()
