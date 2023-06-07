from django.urls import path
from .views import auth, item, shop
urlpatterns = [
    # Region create auth routers
    path('auth/create_user', auth.create_user, name='create_user'),
    path('auth/login_user', auth.login_user, name='login_user'),
    path('users/update_user/<str:id>', auth.update_user, name='update_user'),

    # Region create item routers
    path('items/create_item/<str:shop_id>', item.create_item, name='create_item'),
    path('items/update_item', item.update_item, name='update_item'),
    path('items/delete_item/<str:id>', item.delete_item, name='delete_item'),
    path('items/get_all_items', item.get_all_items, name='get_all_items'),

    # Region create shop routers
    path('auth/create_shop', shop.create_shop, name='create_shop'),
    path('auth/login_shop', shop.login_shop, name='login_shop'),
    path('shops/update_shop', shop.update_shop, name='update_shop'),
    path('shops/delete_shop/<str:id>', shop.delete_shop, name='delete_shop'),
    path('shops/get_all_shop_items/<str:shop_id>', shop.get_all_shop_items, name='get_all_shop_items'),


]
