from django.contrib import admin

from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'ide'
urlpatterns = [

	path('', views.index, name='index'),
	path('run/', views.runCode, name='run'),
	path('code_save/',views.code_save, name='code_save'),
	path('code/',views.code, name='code'),
	path('delete_code/<int:code_id>',views.delete_code, name='delete_code'),
	#----------------User signup and login------------
    path('signup/', views.Signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('user/update/', views.edit_names, name = 'update_user'),

    # Forget Password
    # Change Password
    # if you singhed in then you can use change password but if you are not sign in then use password-reset option
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='commons/change-password.html',
            success_url = '/ide/change-password-complete/'
        ),
        name='change_password'
    ),
    path('change-password-complete/',views.PasswordChangeComplete, name='change_password_complete'),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='commons/password-reset/password_reset.html',
             subject_template_name='commons/password-reset/password_reset_subject.txt',
             email_template_name='commons/password-reset/password_reset_email.html',
             success_url='/ide/password-reset/done/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='commons/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='commons/password-reset/password_reset_confirm.html',
             success_url='/ide/password-reset-complete/'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='commons/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

