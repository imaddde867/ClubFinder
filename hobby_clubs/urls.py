'''Defines URL patterns for hobby_clubs'''
from django.urls import path
from . import views
from .views import logout_view
from .views import all_clubs
# from .views import rate_club
from .views import new_review

app_name = 'hobby_clubs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Detail page for a single club.
    path('clubs/<int:unique_identifier>/', views.club, name='club'),

    # Page for adding a new review.
    path('new_review/<int:unique_identifier>/', views.new_review, name='new_review'),

    # Page for editing an review.
    path('edit_review/<int:unique_identifier>/', views.edit_review, name='edit_review'),

    # Page for adding a new rating.
    # path('rate_club/<int:unique_identifier>/', views.rate_club, name='rate_club'),


    path('search/', views.search_clubs, name='search_clubs'),

    path('logout/', logout_view, name='logout'),

    path('all-clubs/', views.all_clubs, name='all_clubs'),
]
