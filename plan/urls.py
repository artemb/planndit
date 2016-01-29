from django.conf.urls import url, include
from . import views

app_name = 'plan'

urlpatterns = [
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^logout$', views.Logout.as_view(), name='logout'),
    url(r'^register$', views.Register.as_view(), name='register'),

    url(r'^api/', include("plan.api.urls")),

    url(r'^test/', views.TestView.as_view()),

    url(r'^.*$', views.IndexView.as_view(), name='index'),
]
