# your_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Team, Employee
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


# Signup View
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']  # Add this line to get the employee name
        username = request.POST['username']
        password = request.POST['password']

        # Create the user instance
        user = User.objects.create_user(username=username, password=password)

        # Create the employee instance, linking it to the user
        Employee.objects.create(user=user, name=name, username=username)  # Use the appropriate fields

        return redirect('login')
    return render(request, 'signup.html')
# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('team_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Team List View
@login_required
def team_list(request):
    employee = get_object_or_404(Employee, user=request.user)
    teams = employee.teams.all()
    return render(request, 'team_list.html', {'teams': teams})

# Create Team View
@login_required
def create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')  # Retrieve the team name

        # Create the team with the specified name
        team = Team.objects.create(name=team_name)

        # Find the Employee profile associated with the logged-in user
        employee = get_object_or_404(Employee, user=request.user)

        # Add the team to the employee's list of teams
        employee.teams.add(team)

        # Redirect to the list of teams
        return redirect('team_list')
    
    # Render the create team form page
    return render(request, 'create_team.html')

# View to show details of a specific team
@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, teamId=team_id)  # Get team based on teamId
    employee = get_object_or_404(Employee, user=request.user)  # Get the logged-in employee's profile
    
    # Check if the employee is a member of the team
    if team not in employee.teams.all():
        # Render the page with an error if the user isn't a team member
        return render(request, 'team_detail.html', {'error': 'You do not have permission to view this team.'})
    members = team.members.all()
    # Render the team detail page with team context if the user is a team member
    return render(request, 'team_detail.html', {'team': team, 'members' : members})

# Optional: Employee List View
@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def home(request):
    return render(request, 'home.html')


@login_required
def add_members(request, team_id):
    team = get_object_or_404(Team, teamId=team_id)  # Get the specific team
    employees = Employee.objects.exclude(teams=team)  # Employees not in this team yet

    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_employees')  # Get list of selected employee IDs
        selected_employees = Employee.objects.filter(employeeId__in=selected_ids)
        for i in selected_employees:
            i.teams.add(team)
        return redirect('team_detail', team_id=team.teamId)

    query = request.GET.get('q')
    if query:
        employees = employees.filter(Q(name__icontains=query) | Q(username__icontains=query))  # Filter by name or username

    return render(request, 'add_member.html', {'team': team, 'employees': employees})

@login_required
def remove_members(request, team_id):
    team = get_object_or_404(Team, teamId=team_id)
    
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_members')  # Get list of selected member IDs
        selected_members = Employee.objects.filter(employeeId__in=selected_ids)  # Use employeeId for lookup
        
        # Remove each selected employee from the team
        for member in selected_members:
            member.teams.remove(team)
        
        return redirect('team_detail', team_id=team.teamId)

    # Get current team members through the reverse relationship
    members = team.members.all() 
    return render(request, 'remove_member.html', {'team': team, 'members': members})

@login_required
def all_teams(request):
    teams = Team.objects.all()  # Fetch all teams
    return render(request, 'all_teams.html', {'teams': teams})

def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('login')