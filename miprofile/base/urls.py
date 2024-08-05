from django.urls import path
from .views import home, blog, category, upcoming_events

urlpatterns = [
    path('', home, name='home'),
    path('blog/', blog, name='blog'),
    path('category/<int:category_id>/', category, name='category'),
    path('upcoming-events/', upcoming_events, name='upcoming_events'),
]
