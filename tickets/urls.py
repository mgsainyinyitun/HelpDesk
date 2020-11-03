from django.urls import path
from . import views;
#add you path here
urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('<int:id>/',views.ticket_detail,name='ticket-detail'),
    path('<int:id>/<str:status>',views.change_status,name='change-status'),
    path('create',views.create_ticket,name='create-ticket'),
]
