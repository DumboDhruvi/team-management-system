from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    employeeId = models.AutoField(primary_key=True)  # Auto-generated unique ID
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Link to User model, allow null
    name = models.CharField(max_length=255)  # Name of the employee
    username = models.CharField(max_length=150, unique=True)  # Unique username
    password = models.CharField(max_length=255)  # Hashed password
    teams = models.ManyToManyField('Team', related_name='members')  # Many-to-many relationship with Team

    def __str__(self):
        return self.name


class Team(models.Model):
    teamId = models.AutoField(primary_key=True)  # Auto-generated unique ID
    name = models.CharField(max_length=255)  # Name of the team

    def __str__(self):
        return self.name

