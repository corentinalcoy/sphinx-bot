from django.urls import path

from hook.viewsets import HookViewSet

urlpatterns = [
    path('', HookViewSet.as_view({'post': 'post'}), name='hooks'),
]
