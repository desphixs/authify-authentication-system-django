# We import standard Django utilities for handling view logic.
# render: used to load and send HTML templates back to the browser.
# redirect: used to send the user to a different URL (like shifting pages).
from django.shortcuts import render, redirect

# We import the get_user_model function from Django's authentication system.
# Analogy: Instead of hardcoding the import for our User class, get_user_model is like asking
# the settings directory: "Which User blueprint is the active one right now?"
# This is safe and keeps our code completely modular.
from django.contrib.auth import get_user_model

# We call get_user_model to retrieve the active custom User model.
User = get_user_model()

# ==============================================================================
# REAL-WORLD ANALOGY: The Custom Registration View
# ------------------------------------------------------------------------------
# Imagine you are a clerk behind the reception desk of a private members-only club.
# When someone walks up:
# 1. If they just want to look at the registration form (GET request), you hand them the paper form.
# 2. If they fill out the form and submit it to you (POST request), you check their details:
#    - Are all the fields filled in?
#    - Is their email already in the registry?
#    - Is their nickname already taken?
# 3. If everything is valid, you write their details down, securely hide (hash) their password
#    so nobody else can read it, and slide their profile into the physical cabinet (database).
# 4. Once saved, you point them towards the official login entrance (redirect to login page).
# ==============================================================================

# We define the view function to handle user registration.
def register_user(request):
    # We check if the browser sent a POST request (meaning the user clicked "Submit" on the form).
    if request.method == 'POST':
        # We extract the email address directly from the form submission dictionary.
        # .strip() removes any accidental spaces the user might have typed at the start/end.
        email = request.POST.get('email', '').strip()
        # We extract the username nickname from the form submission.
        username = request.POST.get('username', '').strip()
        # We extract the password from the form submission.
        password = request.POST.get('password', '')

        # ---- VALIDATION 1: Ensure all fields are filled in ----
        # If any of the fields are completely empty, we reject the form.
        if not email or not username or not password:
            # We send them back to the form, displaying a clear validation error.
            return render(request, 'register.html', {
                'error': 'All fields are required! Please fill out every box.'
            })

        # ---- VALIDATION 2: Check if email is already registered ----
        # We ask our database if a user record with this exact email already exists.
        if User.objects.filter(email=email).exists():
            # We reload the registration page and inform the user that their email is already in use.
            return render(request, 'register.html', {
                'error': 'A user account with this email address already exists!'
            })

        # ---- VALIDATION 3: Check if username is already taken ----
        # We ask our database if a user record with this exact username nickname already exists.
        if User.objects.filter(username=username).exists():
            # We reload the page and tell them to pick a different nickname.
            return render(request, 'register.html', {
                'error': 'This username is already taken. Please choose a different one!'
            })

        # ---- STEP 4: Creating and saving the User securely ----
        # We use 'create_user' instead of the raw 'User.objects.create()' method.
        # Why? Because 'create_user' automatically hashes the password!
        # Analogy: Password hashing is like locking their plain text password in a heavy-duty
        # safe. Even if someone steals the safe (database breach), they cannot read the password inside!
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # ---- STEP 5: Redirect to the login view ----
        # Now that the user is safely written in our database, we redirect them to the login page.
        # This will point to the URL mapped to the name 'login'.
        return redirect('login')

    # If the request method is GET, it means the user just typed in the URL or refreshed.
    # We simply render the empty HTML registration form.
    return render(request, 'register.html')
