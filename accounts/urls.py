


from django.urls import path,include


app_name = 'accounts'

urlpatterns = [
    path('signup/', include('accounts.urls')),
    path('login/', include('movies.urls')),
    path('logout/', include('community.urls')),
    path('delete/', include('accounts.urls')),
    path('update/', include('movies.urls')),
    path('changepassword/', include('community.urls')),
]
