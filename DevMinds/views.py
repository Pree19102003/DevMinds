from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Resource, Tag, Rating, Comment


# ---------------- HOME ----------------
def home(request):
    resources = Resource.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'resources': resources})


# ---------------- SIGNUP ----------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        college = request.POST['college']
        branch = request.POST['branch']
        semester = request.POST['semester']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)

        Profile.objects.create(
            user=user,
            college=college,
            branch=branch,
            semester=semester
        )

        return redirect('login')

    return render(request, 'signup.html')


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})

    return render(request, 'login.html')


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect('home')


# ---------------- PROFILE ----------------
@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


# ---------------- UPLOAD RESOURCE ----------------
@login_required
def upload_resource(request):
    if request.method == "POST":
        title = request.POST['title']
        subject = request.POST['subject']
        semester = request.POST['semester']
        rtype = request.POST['rtype']
        year = request.POST['year']
        privacy = request.POST['privacy']
        file = request.FILES.get('file')  # SAFE

        if file:
            Resource.objects.create(
                user=request.user,
                title=title,
                subject=subject,
                semester=semester,
                resource_type=rtype,
                year=year,
                privacy=privacy,
                file=file
            )

        return redirect('home')

    return render(request, 'upload.html')


# ---------------- SEARCH ----------------
from django.db.models import Q

def search(request):
    query = request.GET.get('q', '')

    resources = Resource.objects.filter(
        Q(title__icontains=query) |
        Q(subject__icontains=query)
    ) if query else Resource.objects.all()

    return render(request, 'home.html', {'resources': resources})


# ---------------- VIEW / DOWNLOAD RESOURCE ----------------
@login_required
def view_resource(request, id):
    resource = get_object_or_404(Resource, id=id)

    user_rating = Rating.objects.filter(
        user=request.user,
        resource=resource
    ).first()

    user_comment = Comment.objects.filter(
        user=request.user,
        resource=resource
    ).first()

    context = {
        'resource': resource,
        'user_rating': user_rating,
        'user_comment': user_comment
    }

    if resource.privacy == "Public":
        return render(request, 'view_resource.html', context)

    try:
        user_profile = Profile.objects.get(user=request.user)
        owner_profile = Profile.objects.get(user=resource.user)
    except Profile.DoesNotExist:
        return render(request, 'access_denied.html')

    if user_profile.college == owner_profile.college:
        return render(request, 'view_resource.html', context)
    else:
        return render(request, 'access_denied.html')

# ---------------- DELETE REVIEW ----------------
@login_required
def delete_review(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)

    Rating.objects.filter(user=request.user, resource=resource).delete()
    Comment.objects.filter(user=request.user, resource=resource).delete()

    return redirect('view_resource', id=resource_id)


# ---------------- ADD / UPDATE REVIEW ----------------
@login_required
def add_review(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)

    if request.method == "POST":
        stars = request.POST.get('stars')
        comment_text = request.POST.get('comment')

        Rating.objects.update_or_create(
            user=request.user,
            resource=resource,
            defaults={'stars': stars}
        )

        Comment.objects.update_or_create(
            user=request.user,
            resource=resource,
            defaults={'text': comment_text}
        )

    return redirect('view_resource', id=resource_id)
