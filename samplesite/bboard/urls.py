from django.urls import path, include
from .views import index, by_rubric, api_rubrics
from .views import add_and_save, BbDetailView, BbEditView, BbDeleteView, RegistrationView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

# from .views import download

urlpatterns = [
    path('api/rubrics/', api_rubrics),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('add/', add_and_save, name='add'),
    path('', index, name='index'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    # path('download/', download, name='download')
    # path('accounts/password_change/', PasswordChangeView.as_view(
    #         template_name='registration/password_change_form.html'
    #     ), name='password_change'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/',
         PasswordResetConfirmView, name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView,
         name='password_reset_complete'),
    # path('auth/', include('rest_framework_social_oauth2.urls', name='vk')),
    # path('social/', include('social_django.urls', namespace='social')),
    # path('auth/', include('rest_framework_social_oauth2.urls')),
]
