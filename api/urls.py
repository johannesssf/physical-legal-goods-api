from django.urls import include, path

from api import views


urlpatterns = [
    path('physical-people/', views.physical_people_list),
    path('physical-people/<int:id>/', views.physical_people_detail),
]
