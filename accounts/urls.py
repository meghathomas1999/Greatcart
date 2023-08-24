from django.urls import path
from  . import views

urlpatterns=[

path('register/', views.register,name='register'),
path('login/', views.login,name='login'),
path('logout/', views.logout,name='logout'),
path('dashboard/', views.dashboard,name='dashboard'),
path('', views.dashboard,name='dashboard'),
path('activate/<uidb64>/<token>', views.activate,name='activate'),
path('forgotpassword/', views.forgotpassword,name='forgotpassword'),
path('Reset_Password_Validate/<uidb64>/<token>', views.Reset_Password_Validate,name='Reset_Password_Validate'),
path('resetpassword/', views.resetpassword,name='resetpassword'),

]