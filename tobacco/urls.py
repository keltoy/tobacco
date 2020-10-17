"""tobacco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from regulatory_system import views as rs_views
from file_upload import views as fu_views
from file_upload.views import UploadFlowView, UploadFlowDetailView, UploadCustomerView
from login import views as login_views

router = routers.DefaultRouter()
router.register(r'users', login_views.UserViewSet)
router.register(r'groups', login_views.GroupViewSet)
router.register(r"customer", rs_views.CustomerViewSet)
router.register(r"customer_latest", rs_views.CustomerLatestViewSet)
router.register(r"flow", rs_views.AbnormalFlowViewSet)
router.register(r"flow_detail", rs_views.AbnormalFlowDetailViewSet)
router.register(r'upload', fu_views.RelevantDocumentViewSet)
router.register(r'presentation', fu_views.PresentationViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('import/flow/', UploadFlowView.as_view()),
    path('import/flow/detail/', UploadFlowDetailView.as_view()),
    path('import/customer/', UploadCustomerView.as_view()),
    path('tinymce/', include('tinymce.urls'))
]
