from django.urls import path
from .views import ItemCreateView, ItemDetailView, ItemUpdateView, ItemDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT Token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # CRUD for items
    path('items/', ItemCreateView.as_view(), name='create-item'),
    path('items/get/<int:pk>/', ItemDetailView.as_view(), name='detail-item'),
    path('items/update/<int:pk>/', ItemUpdateView.as_view(), name='update-item'),
    path('items/delete/<int:pk>/', ItemDeleteView.as_view(), name='delete-item'),
]
