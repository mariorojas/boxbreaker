from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('', views.GameFormView.as_view(), name='new'),
    path('<uuid:uuid>/', views.GameDetailView.as_view(), name='detail'),
    path(
        '<uuid:uuid>/attempts/', views.AttemptCreateView.as_view(), name='new-attempt'
    ),
]
