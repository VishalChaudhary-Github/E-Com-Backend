from django.urls import path
from api import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('account/deactivate/', views.AccountDeactivateView.as_view(), name='account-deactivate'),
    path('account/activate/', views.ReActivateAccountView.as_view(), name='account-activate'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    path('customer/', views.CustomerView.as_view(), name='view-customer'),
    path('customer/create/', views.CreateCustomerView.as_view(), name='create-customer'),
    path('customer/update/', views.UpdateCustomerView.as_view(), name='update-customer'),
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    path('product/', views.ProductListView.as_view(), name='products-list'),
    path('product/add/', views.AddProductView.as_view(), name='add-product'),
    path('product/update/<int:product_id>', views.UpdateProductView.as_view(), name='update-product'),
    path('product/delete/<int:product_id>', views.DeleteProductView.as_view(), name='delete-product'),
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    path('category/', views.CategoryListView.as_view(), name='categories-list'),
    path('category/add/', views.AddCategoryView.as_view(), name='add-category'),
    path('category/delete/<int:category_id>', views.DeleteCategoryView.as_view(), name='delete-category'),
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    path('add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', views.ListCartView.as_view(), name='view-cart'),
    path('remove-from-cart/<int:product_id>', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    path('place-order/', views.PlaceOrderView.as_view(), name='place-order')
]