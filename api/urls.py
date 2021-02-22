from django.urls import include, path

from api import views


urlpatterns = [
    path('physical-people/', views.physical_people_list),
    path('physical-people/<int:id>/', views.physical_people_detail),
    path('legal-people/', views.legal_people_list),
    path('legal-people/<int:id>/', views.legal_people_detail),
    path('goods/', views.goods_list),
    path('goods/<int:id>/', views.goods_detail),
]
