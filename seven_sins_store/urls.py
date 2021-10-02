
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from orders.views import cart, track
from products.views import ProductDetailView, ProductListView
from seven_sins_store.views import info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<slug:slug>', ProductDetailView.as_view(), name='view'),
    path('', ProductListView.as_view(), name='home'),
    path('cart/', cart, name='cart'),
    path('orders/', include(('orders.urls', 'orders'))),
    path('track/<int:pk>', track, name='track'),
    path('info/', info, name='info')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
