"""
URL configuration for SolarEnergyAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from SolarPlants import views
from django.urls import include, path
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()

router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('items/', views.ItemList.as_view(), name='items-list'),
    path('items/add/', views.add_item, name='create_item'),
    path('items/<int:item_id>/', views.ItemDetail.as_view(), name='items-detail'),
    path('items/add2plant/<int:item_id>/<int:plant_id>/', views.add2plant, name='add2plant'),
    path('item2plant/', views.item2plant.as_view(), name='item2plant'),
    path('plants/', views.PlantList.as_view(), name='plant-list'),
    path('plants/<int:plant_id>/', views.PlantDetail.as_view(), name='plant-detail'),
    path('plants/<int:plant_id>/forming/', views.plant_forming, name='plant-forming'),
    path('plants/<int:plant_id>/finishing/', views.plant_finishing, name='plant-finishing'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'admin/', admin.site.urls),
    #path('users/', views.UsersList.as_view(), name='users-list'),
    #path('users/<int:user_id>/', views.UsersList.as_view(), name='users-edit'),
    #path('users/logout/', views.user_logout, name='users-edit'),
    #path('users/login/', views.user_login, name='users-edit'),
    path('users/login/',  views.login_user, name='login'),
    path('users/logout/', views.logout_user, name='logout'),
    path('users/create/', views.create_user, name='logout'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
