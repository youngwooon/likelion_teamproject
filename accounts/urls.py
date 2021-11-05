from django.urls import path
from accounts.views import signup, login, logout, history

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('history/', history, name='history'),
]