from django.urls import path

urlpatterns = [
    path('url/', TestView.as_view(), name='the_url'),
]
