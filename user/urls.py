from django.urls import path
from . import views;
from django.contrib.auth import views as auth 
from .forms import LoginForm;

urlpatterns = [
    #path('login/',views.login,name="login"),
    path('login/',auth.LoginView.as_view(authentication_form=LoginForm),name='login'),
    path('logout/',auth.LogoutView.as_view(),name='logout'),
    path('password_change/',auth.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/',auth.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password_reset/',auth.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('register/',views.register,name='register'),
    path('edit/',views.edit,name='edit'),
    path('tech/',views.tech_view,name='tech-view'),
    path('tech/<str:role>',views.role_view,name='role-view'),
    path('tech/detail/<int:id>',views.user_detail_view,name='user-detail-view'),
    path('tech/detail/delete/<int:id>',views.user_delete,name='user-delete'),
    #customer
    path('customer/',views.customer_view,name='customer-view'),
    path('customer/new',views.new_customer,name='new-customer'),

    #error
    path('system/error',views.error,name='error'),
    path('system/contact-us',views.contactus,name='contact-us'),
    #path('dashboard/',views.dashboard,name='dashboard'),
]
