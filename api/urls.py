from django.urls import path
from .views import auth, item
urlpatterns = [
    # Region create auth routers
    path('auth/create_user', auth.create_user, name='create_user'),
    path('auth/login_user', auth.login_user, name='login_user'),
    path('auth/update_user/<str:id>', auth.update_user, name='update_user'),

    # Region create item routers
    path('auth/items/create_item', item.create_item, name='create_item'),
    path('auth/items/update_item', item.update_item, name='update_item'),
    path('auth/items/delete_item/<str:id>', item.delete_item, name='delete_item'),

]
