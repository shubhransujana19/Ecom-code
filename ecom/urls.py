from django.urls import path

from .import views

urlpatterns = [
	#Leave as empty string for base url

	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('userreg/', views.userReg, name='usr-reg-page'),
    path('userlog/', views.userLogin, name='usr-log-page'),
	path('userchangpass/', views.userChngPass, name='usr-ChngPass-page'),
	path('userprofile', views.userChngProfile, name='usr-ChngProfile-page'),
    path('userlogout/', views.userLogout, name='usr-logout-page'),
	path('about/',views.about, name='about'),
	path('contactus/',views.contactus, name='contactus'),
	
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="update_item"),
]