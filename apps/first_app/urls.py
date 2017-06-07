from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^session$', views.log_in),
    url(r'^users$', views.create_user),
    url(r'^log_out$', views.log_out),
    url(r'^clock_in$', views.clock_in),
    url(r'^clock_out$', views.clock_out),
    url(r'^sudo$', views.admin),
    url(r'^create_message$', views.create_message),
    url(r'^delete_message/(?P<id>\d+)$', views.delete_message)






]
