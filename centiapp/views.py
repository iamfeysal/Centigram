from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , Http404
from .models import Image , Profile , Comment
from .forms import EditProfileForm , UploadForm , CommentForm
from django.contrib.auth.models import User


# Create your views here.
@login_required( login_url='/accounts/login/' )
def home(request):
    '''
    Method that fetches all images from all users.
    '''
    current_user=request.user
    profile=Profile.get_profile( )
    image=Image.get_images( )
    comments=Comment.get_comment( )
    return render( request , 'index.html' , {
        "profile": profile ,
        "comments": comments ,
        "current_user": current_user ,
        "images": image , } )


@login_required( login_url='/accounts/login/' )
def profile(request):
    '''
    	Method that fetches a users profile page
    	'''
    current_user=request.user
    profile=Profile.get_profile( )
    image=Image.get_images( )
    comments=Comment.get_comment( )
    return render( request , 'profile/profile.html' , {
        "comments": comments ,
        "image": image ,
        "user": current_user ,
        "profile": profile , } )


@login_required( login_url='/accounts/login/' )
def settings(request):
    '''
    	Method that fetches the details of a user uniquily
    	'''
    settings=Profile.get_profile( )
    return render( request , 'profile/setting.html' , {"settings": settings} )


@login_required( login_url='/accounts/login/' )
def edit(request):
    current_user=request.user
    if request.method == 'POST':
        form=EditProfileForm( request.POST , request.FILES )
        if form.is_valid( ):
            update=form.save( commit=False )
            update.user=current_user
            update.save( )
            return redirect( 'profile' )
    else:
        form=EditProfileForm( )
    return render( request , 'profile/edit.html' , {
        "form": form} )


@login_required( login_url="/accounts/login/" )
def upload(request):
    '''
    	Method that return a form for uploading images
    	'''
    current_user=request.user
    profiles=Profile.get_profile( )
    for profile in profiles:
        if profile.user.id == current_user.id:
            if request.method == 'POST':
                form=UploadForm( request.POST , request.FILES )
                if form.is_valid( ):
                    upload=form.save( commit=False )
                    upload.user=current_user
                    upload.profile=profile
                    upload.save( )
                    return redirect( 'home' )
            else:
                form=UploadForm( )
            return render( request , 'upload/new-upload.html' , {
                "user": current_user ,
                "form": form} )


@login_required( login_url="/accounts/login/" )
@login_required( login_url='/accounts/login/' )
def search(request):
    '''
	Method that searches for users based on their profiles
	'''
    if request.GET['search']:
        search_term=request.GET.get( "search" )
        profiles=Profile.objects.filter( user__username__icontains=search_term )
        message=f"{search_term}"

        return render( request , 'search.html' , {"message": message , "profiles": profiles} )
    else:
        message="You haven't searched for any item"
        return render( request ,'search.html' , {"message": message} )


@login_required( login_url='/accounts/login/' )
def new_comment(request , pk):
    '''
    	Method that fetches a users new comment from the comment form
    	'''
    image=get_object_or_404( Image , pk=pk )
    current_user=request.user
    if request.method == 'POST':
        form=CommentForm( request.POST )
        if form.is_valid( ):
            comment=form.save( commit=False )
            comment.image=image
            comment.user=current_user
            comment.save( )
            return redirect( 'home' )
    else:
        form=CommentForm( )
    return render( request , 'comment.html' , {"user": current_user ,
                                               "comment_form": form} )


@login_required( login_url="/accounts/login/" )
def view_profile(request , pk):
    '''
    	Method that dispalys users profile only after creating profile
    	'''
    current_user=request.user
    image=Image.get_images( )
    profile=Profile.get_profile( )
    comment=Comment.get_comment( )
    user=get_object_or_404( User , pk=pk )
    return render( request , 'profile/view-profile.html' , {"user": current_user ,
                                            "images": image ,
                                            "my_user": user ,
                                            "comments": comment ,
                                            "profile": profile} )


@login_required( login_url="/accounts/login/" )
def like(request , operation , pk):
    '''
    Method function that likes a post.
    '''
    image=get_object_or_404( Image , pk=pk )
    if operation == 'like':
        image.likes+=1
        image.save( )
    elif operation == 'unlike':
        image.likes-=1
        image.save( )
    return redirect( 'home' )
