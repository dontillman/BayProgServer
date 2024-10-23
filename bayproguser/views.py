from django.shortcuts import render
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UserAdmin

from PIL import Image

from .admin import UserCreationForm, UserChangeForm
from .models import BayProgUserManager, BayProgUser

import logging
logger = logging.getLogger('django')

def signup(request):
    logger.debug('views.py: signup')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request,
                  'registration/signup.html',
                  {'form': form,
                   'table': form.as_table()})


## here:
def edit(request):
    # reminder
    # logger.debug('message')
    thumbnailsize = 96, 96
    message = ''
    form = None
    if request.method == 'POST':
        logger.debug('*** post section')
        form = UserChangeForm(data=request.POST,
                              files=request.FILES,
                              instance=request.user)
        if form.is_valid():
            logger.debug('form is valid')
            form.save()
            logger.debug('form saved')
            if request.user.image:
                imagefile = request.user.image.file
                with Image.open(imagefile) as im:
                    im.thumbnail(thumbnailsize)
                    im.save(imagefile.name)
            message = 'User updated'
    if not form:
        form = UserChangeForm(instance=request.user)
    context = {'message': message,
               'user': request.user,
               'fullname': request.user.get_full_name(),
               'form': form,
               'table': form.as_table(),
               'email': request.user.email}
    return render(request, 'registration/edit.html', context)

def user(request, id=0):
    logger.debug('user called', id)
    userentry = BayProgUser.objects.get(id=id)
    context = {'user': userentry,
               'fullname': userentry.get_full_name()}
    return render(request, 'registration/user.html', context)


def editPREV(request):
    # reminder
    # logger.debug('message')
    thumbnailsize = 96, 96
    userform = None
    passwordform = None
    message = ''
    if request.method == 'POST':
        logger.debug('*** post section')
        savetype = request.POST['update']
        if 'user' == savetype:
            userform = UserChangeForm(request.POST,
                                      request.FILES,
                                      instance=request.user)
            if userform.is_valid():
                userform.save()
                imagefile = request.user.image.file
                with Image.open(imagefile) as im:
                    im.thumbnail(thumbnailsize)
                    im.save(imagefile.name)
                message = 'User updated'
        elif 'password' == savetype:
            passwordform = PasswordChangeForm(user=request.user,
                                      data=request.POST)
            logger.debug('password form')
            logger.debug(passwordform)
            if passwordform.is_valid():
                logger.debug('form is valid')
                passwordform.save()
                logger.debug('form saved')
                update_session_auth_hash(request, passwordform.user)
                logger.debug('updated hash thing')
                message = 'Password updated'
                logger.debug('and done')
            logger.debug('after valid check')
    if not userform:
        userform = UserChangeForm(instance=request.user)
    if not passwordform:
        passwordform = PasswordChangeForm(request.user)
    context = {'message': message,
               'user': request.user,
               'fullname': request.user.get_full_name(),
               'userform': userform,
               'usertable': userform.as_table(),
               'email': request.user.email,
               'passwordform': passwordform,
               'passwordtable': passwordform.as_table()}
    return render(request, 'registration/edit.html', context)

