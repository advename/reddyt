from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import validators


def login(request):
    # context is used to return error messages
    context = {}

    '''
   Check if it's a POST request, if true, it means that the
   form has been filled out and somebody tried to log in
   else, if it is different than a POST request, it means that
   the page has been opened to log in. In that case
   we simply return the login.html file as seen in line 19    
    '''
    if request.method == "POST":
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])

        # The user instance returns True or False if the username/password combination if valid.
        if user:
            # Place a session cookie to login the user
            dj_login(request, user)
            return HttpResponseRedirect(reverse('discussion_app:index'))

        # Handle failed login attempts
        else:
            # Update the context dictionary with an error message
            context = {"error_message": "Invalid username/password combination"}

    # Return the login.html page with a context if it exists.
    return render(request, 'account_app/login.html', context)


def sign_up(request):
    # Initialize context for error messages
    context = {}

    # Redirect the user if they are already logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('discussion_app:index'))

    # Check if POST request -> a user tries to create a new account
    if request.method == "POST":
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        username = request.POST['username']
        email = request.POST['email']

        if not password == confirm_password:
            # Passwords didn't match
            context = {
                'error_message': 'Passwords did not match. Please try again.'
            }

        elif not validators.email(email):
            # Invalid email
            context = {
                'error_message': 'Invalid email.'
            }

        else:
            # All checks passed, create new user.
            # Create new user and check if it was successfull
            if User.objects.create_user(username, email, password):
                return HttpResponseRedirect(reverse('account_app:login'))
            else:
                # User creation failed
                context = {
                    'error_message': 'Could not create user account - please try again.'
                }

    # Return the signup form or return it with an error message from a failed registration
    return render(request, 'account_app/sign_up.html', context)


@login_required
def user(request):
    context = {}
    status_message = None
    if 'status_message' in request.session:
        context = {"status_message": request.session['status_message']}
        del request.session['status_message']
    return render(request, 'account_app/user_page.html', context)


@login_required
def update_password(request):
    # response messages are stored in session

    if request.method == "POST":
        user = authenticate(
            request, username=request.user.username, password=request.POST["old_password"])

        # The user instance returns True or False if the username/password combination if valid.
        if user:
            # New Passwords do not match
            if not request.POST["new_password1"] == request.POST["new_password2"]:
                status_message = "Passwords do not match"

            # Update with new password
            user.set_password(request.POST["new_password1"])
            user.save()
            status_message = "Password updated"

        # Handle failed login attempts
        else:
            # Update the context dictionary with an error message
            status_message = "Invalid password"

    # Return the login.html page with a context if it exists.
    request.session['status_message'] = status_message
    return redirect("account_app:user")


def logout(request):
    dj_logout(request)
    return HttpResponseRedirect(reverse('discussion_app:index'))


@login_required
def delete(request):
    # delete user
    request.user.delete()
    return HttpResponseRedirect(reverse('account_app:logout'))
