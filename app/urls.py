from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MypasswordResetForm,MySetPasswordForm

urlpatterns = [
    
    path('', views.ProductViews.as_view(),name="home"),
    path('product-detail/<int:pk>/',views.ProductDetailView.as_view(), name='ProductDetailView'),

    # cart sections 

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart_show, name='cartshow'),
    path('checkout/', views.check_out, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

    path('Payment_Form/', views.payment_view, name='Payment_Form'),
    path('payment-success/',views.success_view, name='success_url_name'),





    # PRODUCT ADD # MINUS CART # remove CART 
    path('pluscart/', views.pluscart),

    path('minuscart/', views.minuscart),

    path('removecart/', views.remove_cart,name='removecart'),


    

    #informations section 
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),

    #order confirm

    

   #login and registrations section 

    path('registration/', views.CustomerRegistrationView.as_view(), name='CustomerRegistration'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm ), name='login'),

    path('logout/', auth_views.LogoutView.as_view (next_page = 'home'), name='logoutpage'),


    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name = 'app/changepassword.html',form_class = MyPasswordChangeForm,success_url='/passwordchangedone/'), name='password_change'),

    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/changepassworddone.html'), name='passwordchangedone'),
    
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MypasswordResetForm, email_template_name='app/password_reset.html', subject_template_name='app/password_reset.html', success_url='/password_reset_done/'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complate/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_confirm_complate.html'), name='passwordchangedone'),

    path('changepassword/', views.change_password, name='changepassword'),





    # page sections 

    path('buy/', views.buy_now, name='buy-now'),

    path('mobile/', views.mobile, name='mobile'),

 







    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



