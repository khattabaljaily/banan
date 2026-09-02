from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('portfolio/banan-ims/', views.BananIMSProductView.as_view(), name='product_banan_ims'),
    path('portfolio/banan-bcms/', views.BananBCMSProductView.as_view(), name='product_banan_bcms'),
    path('products/', views.ProductsIndexView.as_view(), name='products'),
    path('portfolio/', views.PortfolioListView.as_view(), name='portfolio'),
    path('portfolio/<slug:slug>/', views.PortfolioDetailView.as_view(), name='project_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
