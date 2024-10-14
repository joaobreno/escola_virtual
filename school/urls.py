from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import EstudanteViewSet

router = DefaultRouter()
router.register(r'api/estudantes', EstudanteViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('add-student/', views.edit_student, name='add-student'),
    path('edit-student/<int:id>', views.edit_student, name='edit-student'),
    path('delete-student/ajax/', views.delete_student, name='delete-student'),
    path('logout/', views.quick_logout, name='quick_logout'),

    path('', include(router.urls)),
]