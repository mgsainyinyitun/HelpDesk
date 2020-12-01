from django.urls import path
from . import views;
#add you path here
urlpatterns = [
	#dashboard
    path('',views.dashboard,name='dashboard'),
    path('<int:id>/',views.ticket_detail,name='ticket-detail'),
    path('<int:id>/<str:status>',views.change_status,name='change-status'),
    path('<int:id>/category/<slug:category>',views.change_category, name='change-category'),
    path('create',views.create_ticket,name='create-ticket'),
    path('status/<str:status>',views.status_view,name='status-view'),
    #category
    path('category/new',views.new_category,name='new-category'),
    #tickets
    path('tickets',views.tickets,name='tickets'),
]
