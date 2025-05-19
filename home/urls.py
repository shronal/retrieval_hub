from django.contrib import admin
from django.urls import path, include
from home import views
from .views import rli
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('rli/', rli, name='rli'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
]


#Django admin customization by SHRONAL
admin.site.site_header = "The Developer Shronal aka BlackBlood"
admin.site.site_title = "Swagat toh karo aapna Dashboard ko"
admin.site.index_title = "Oilcome"

urlpatterns = [
    path('', views.LoginPage, name = 'Login Page'),
    path('signup', views.SignupPage, name = 'Signup Page'),
    path('login', views.LoginPage, name = 'Login Page'),
    path('logout', views.LoginPage, name = 'Logout Page'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password_view'),
    path('userpp', views.UserPP, name = 'userpp'),
    path('home', views.home, name = 'home'),
    path('about', views.about, name = 'about'),
    path('projects', views.projects, name = 'projects'),
    path('contact', views.contact, name = 'contact'),
    path('rli', views.rli, name = 'rli'),
    path('rfi', views.rfi, name = 'rfi'),
    path('success', views.success, name='success'),
    path('success1', views.success1, name='success1'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('list-reports/', views.list_reports, name='list_reports'),
    path('edit-report/<int:pk>/<str:report_type>/', views.edit_report, name='edit_report'),
    path('available-reports/', views.available_reports, name='available_reports'),
    path('item/<str:model_type>/<int:item_id>/', views.item_detail, name='item_detail'),
    path('get-item-details/<str:type>/<int:pk>/', views.get_item_details, name='get_item_details'),
    path('claim/<str:model_name>/<int:item_id>/', views.claim_item, name='claim_item'),
    path('get_item_details/<str:item_type>/<int:item_id>/', views.get_item_details, name='get_item_details'),
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url='/'
    ), name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
    # path('success', TemplateView.as_view(template_name='success.html'), name='success'),

