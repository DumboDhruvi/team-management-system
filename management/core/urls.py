# your_app/urls.py

from django.urls import path
from .views import signup, login_view, team_list, create_team, team_detail, employee_list, home, add_members, remove_members, all_teams, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signin/', login_view, name='login'),
    path('teams/', team_list, name='team_list'),
    path('teams/create/', create_team, name='create_team'),
    path('teams/<int:team_id>/', team_detail, name='team_detail'),
    path('employees/', employee_list, name='employee_list'),
    path('teams/<int:team_id>/add-members/', add_members, name='add_members'),
    path('teams/<int:team_id>/remove-members/', remove_members, name='remove_members'),
    path('all_teams/', all_teams, name='all_teams'),
    path('logout/', logout_view, name='logout'),
]
