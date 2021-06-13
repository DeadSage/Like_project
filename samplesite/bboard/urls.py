from django.urls import path
from .views import index, by_rubric
from .views import add_and_save, BbDetailView, BbEditView, BbDeleteView, RegistrationView
from django.contrib.auth.views import PasswordChangeView

# from .views import download

urlpatterns = [
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('add/', add_and_save, name='add'),
    path('', index, name='index'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    # path('download/', download, name='download')
    path('accounts/password_change/', PasswordChangeView.as_view(
            template_name='registration/password_change_form.html'
        ), name='password_change'),
]
