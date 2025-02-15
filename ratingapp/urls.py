from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('rate/<int:movie_id>/', views.rate_movie, name='rate_movie'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('dummy_date_insert/',views.dummy_date_insert,name='dummy_date_insert'),
]
