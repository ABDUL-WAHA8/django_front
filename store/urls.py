from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('check_db_query/', views.check_db_query),
    path('get_com_accounts/', views.get_com_accounts),
    path('get_null_featured_product/', views.get_null_featured_product),
    path('get_low_inventory/', views.get_low_inventory),
    path('get_argu_values/',views.get_argu_values),
    path('sortings/',views.sortings),
    path('finding_ordered_products/',views.finding_ordered_products),
    path('orders_n_customers/',views.orders_n_customers),
    path('get_customers_full_name/',views.get_customers_full_name),
    path('get_tag_products/',views.get_tag_products),
    path('inserting_data/',views.inserting_data),
    path('updating_data/',views.updating_data),
    path('product_list/',views.product_list),
    path('customer_list/',views.customer_list),
    path('product_individually/<int:id>/',views.product_individually)
]