from django.urls import path
from . import views


urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="home"),
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('search/', views.search, name = 'search'),
    path('rastreio/', views.rastreio, name = 'rastreio'),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    
	path('produto/detail/<int:productId>', views.singleProduto, name="singleProduto"),

]