from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from feedback.views import feedback
from orders.views import cart
from products.views import ProductDetailView, ProductListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authorization/', include(('authorization.urls', 'authorization'))),
    path('<str:slug>/<int:pk>', ProductDetailView, name='view'),
    path('', ProductListView.as_view(), name='home'),
    path('orders/', include(('orders.urls', 'orders'))),
    path('cart/', cart, name='cart'),
    path('manager/', include(('manager.urls', 'manager'))),
    path('feedback/', feedback, name='feedback'),
    path('api/v1/', include('api_1.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = "seven_sins_store.views.bad_request_view"
handler403 = "seven_sins_store.views.permission_denied_view"
handler404 = "seven_sins_store.views.not_found_view"
handler500 = "seven_sins_store.views.server_error_view"
