from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rango import views
from rango.views import AboutView, AddCategoryView, ProfileView

# Add namespace for URL referencing
app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    # path('about/', views.about, name='about'),
    path('about/', AboutView.as_view(), name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    # path('add_category/', views.add_category, name='add_category'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('category/<category_name_slug>/add_page/', views.add_page, name='add_page'),
    # path('search/', views.search, name='search'),
    path('goto/', views.goto_url, name='goto'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', ProfileView.as_view(), name='profile'),
    path('profiles/', views.list_profiles, name='list_profiles'),
    path('like/', views.like_category, name="like_category"),
    path('suggest/', views.suggest_category, name="suggest_category"),
    path('add/', views.auto_add_page, name='auto_add_page')
    # path('register/', views.register, name='register')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
