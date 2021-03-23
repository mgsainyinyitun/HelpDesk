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
    path('category/delete/<slug:cat>',views.delete_category,name='delete-category'),
    path('category/edit/<slug:cat>',views.edit_category,name='edit-category'),
    #tickets
    path('tickets',views.tickets,name='tickets'),
    path('tickets/pdf',views.render_pdf,name='render-pdf'),
    path('tickets/csv',views.export_csv,name='export-csv'),
    path('tickets/date/clear',views.clear_date,name='clear-date'),
    #tickets detail
    path('ticket/pdf/<int:id>',views.ticket_detail_pdf,name='ticket-detail-pdf')
]
