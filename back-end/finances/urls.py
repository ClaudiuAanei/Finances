from django.urls import include, path
from finances.api.views import dashboard, transactions, upload
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"dashboard", dashboard.DashboardView, basename="dashboard")
router.register(r"transactions", transactions.TransactionsView, basename="transactions")
router.register(r"upload", upload.UploadView, basename="upload")

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    
]