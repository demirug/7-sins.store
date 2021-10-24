from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from feedback.views import feedback
from orders.views import cart, TrackView
from products.views import ProductDetailView, ProductListView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('authorization/', include(('authorization.urls', 'authorization'))),
    path('<str:slug>/<int:pk>', ProductDetailView, name='view'),
    path('', ProductListView.as_view(), name='home'),
    path('orders/', include(('orders.urls', 'orders'))),
    path('cart/', cart, name='cart'),
    path('track/<int:pk>', TrackView.as_view(), name='track'),
    path('manager/', include(('manager.urls', 'manager'))),
    path('feedback/', feedback, name='feedback'),
    path('api/v1/', include('api_1.urls'))
]

handler400 = "seven_sins_store.views.bad_request_view"
handler403 = "seven_sins_store.views.permission_denied_view"
handler404 = "seven_sins_store.views.not_found_view"
handler500 = "seven_sins_store.views.server_error_view"
