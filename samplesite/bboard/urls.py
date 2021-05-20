from django.urls import path
from .views import index, by_rubric
from .views import add_and_save, BbDetailView, BbEditView, BbDeleteView

# from .views import download

urlpatterns = [
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('add/', add_and_save, name='add'),
    path('', index, name='index'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete')
    # path('download/', download, name='download')
]
