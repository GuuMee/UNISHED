from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save() #we are grabbing the user form and save it
            user.set_password(user.password) #we are hasing the password and save it
            user.save() #we save those changes to the user

            profile = profile_form.save(commit=False) #I don't want to commit to the database, otherwise I may get errors with collisions. Instead we use one to one relationship
            profile.user = user #onetoone relationship is defined in the views.py file

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'login_user/registration.html',
                            {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})
