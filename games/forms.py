import json
import random
import string

from django import forms
from django.apps import apps
from django.conf import settings
from django.core.validators import MinLengthValidator, RegexValidator

from .models import Attempt, Game
from .schemas import AttemptSchema


# attempts & points
POINTS = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
}


def get_computed_answer(answer, parent_answer):
    return str(['*' if a == b else b for a, b in zip(answer, parent_answer)])


class AttemptForm(forms.ModelForm):
    answer = forms.CharField(
        max_length=settings.ANSWER_LENGTH,
        validators=[
            MinLengthValidator(settings.ANSWER_LENGTH),
            RegexValidator('^\\d+$')
        ],
    )

    class Meta:
        model = Attempt
        fields = ['answer']

    def clean_answer(self):
        answer = self.cleaned_data.get('answer')
        return answer

    def save(self, commit=True):
        answer = self.cleaned_data.get('answer')
        parent = self.instance.parent

        # check answer
        if answer == parent.answer:
            nodes = [{'guess': g, 'correct': True, 'exists': True} for g in answer]
            parent.completed = parent.win = True
            parent.save()
        else:
            # replace the correct digits with asterisks
            computed = get_computed_answer(answer, parent.answer)

            # check remain digits
            nodes = []
            for guess, digit in zip(answer, parent.answer):
                correct = guess == digit

                nodes.append({
                    'guess': guess,
                    'correct': correct,
                    'exists': correct or guess in computed,
                })

                # remove misplaced digits in computed answer
                if not correct:
                    computed = computed.replace(guess, '*', 1)

        # save attempt result in json format
        schema = AttemptSchema()
        self.instance.result = json.dumps([schema.dump(n) for n in nodes])

        # check num of attempts, including the current one
        attempts = parent.attempts.all().count() + 1
        if attempts >= settings.ATTEMPTS_LIMIT:
            parent.completed = True
            parent.save()

        # update points for the game and user
        if parent.win and parent.owner:
            points = POINTS.get(attempts)

            parent.points = points
            parent.save()

            profile_model = apps.get_model('profiles', 'Profile')
            profile, created = profile_model.objects.get_or_create(owner=parent.owner)
            profile.score += points
            profile.save()

        return super().save(commit)


class GameForm(forms.Form):
    def save(self, owner=None, ip_address=None):
        answer = ''.join(
            [random.choice(string.digits) for _ in range(settings.ANSWER_LENGTH)]
        )
        instance = Game(answer=answer, owner=owner, ip_address=ip_address)
        instance.save()
        return instance
