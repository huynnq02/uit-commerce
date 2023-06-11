from django.urls import path
from .views import auth, item, shop, review, report, bill, order, category
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

    # Region create category routers
    path('categories/create_category', category.create_category, name='create_category'),
    path('categories/update_category/<str:id>', category.update_category, name='update_category'),
    path('categories/delete_category/<str:id>', category.delete_category, name='delete_category'),
    path('categories/get_all_categories', category.get_all_categories, name='get_all_categories'),
    path('categories/get_category/<str:id>', category.get_category, name='get_category'),

     # Region create report routers
    path('reports/create_report', report.create_report, name='create_report'),
    path('reports/update_report/<str:id>', report.update_report, name='update_report'),
    path('reports/delete_report/<str:id>', report.delete_report, name='delete_report'),
    path('reports/get_all_reports', report.get_all_reports, name='get_all_reports'),
    path('reports/get_report/<str:id>', report.get_report, name='get_report'),

    # Region create review routers
    path('reviews/create_review', review.create_review, name='create_review'),
    path('reviews/update_review/<str:id>', review.update_review, name='update_review'),
    path('reviews/delete_review/<str:id>', review.delete_review, name='delete_review'),
    path('reviews/get_all_reviews', review.get_all_reviews, name='get_all_reviews'),
    path('reviews/get_review/<str:id>', review.get_review, name='get_review'),

    # Region create bill routers
    path('bills/create_bill', bill.create_bill, name='create_bill'),
    path('bills/update_bill/<str:id>', bill.update_bill, name='update_bill'),
    path('bills/delete_bill/<str:id>', bill.delete_bill, name='delete_bill'),
    path('bills/get_all_bills', bill.get_all_bills, name='get_all_bills'),
    path('bills/get_bill/<str:id>', bill.get_bill, name='get_bill'),

]
