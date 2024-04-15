import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
# from django.db.models import Avg  
# from django.http import HttpResponse

from .models import Club, Like
from .forms import ReviewForm, RatingForm
from django.http import JsonResponse

def index(request):
    """The home page for Hobby Log."""
    return render(request, 'hobby_clubs/index.html')


@login_required

def all_clubs(request):
    clubs = Club.objects.all()  # 获取所有的数据库记录
    return render(request, 'hobby_clubs/all_clubs.html', {'clubs': clubs})




from django.shortcuts import get_object_or_404







@login_required
def science_clubs(request):
    science_clubs = Club.objects.filter(category='science')
    return render(request, 'hobby_clubs/science_clubs.html', {'science_clubs': science_clubs})










def search_clubs(request):
    if request.method == 'GET':
        # 获取用户提交的搜索条件
        postal_code = request.GET.get('postcode')
        age = request.GET.get('age')
        club_type = request.GET.get('clubtype')
        
        matching_clubs = []

        with open('databasestore/clubs-info.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (postal_code == row['Postal_Code'] and
                    age == row['Age'] and
                    club_type == row['Category']):
                    matching_clubs.append(row)
        if not matching_clubs:
            message = "Apologies, there are currently no clubs that match your criteria. Please try different search criteria."
            return render(request, 'hobby_clubs/search_results.html', {'message': message})
        
        return render(request, 'hobby_clubs/search_results.html', {'matching_clubs': matching_clubs})

from django.contrib.auth import logout

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        print("用户已注销")
        return redirect('hobby_clubs:index')
    return redirect('hobby_clubs:index') 
    
from django.shortcuts import render, get_object_or_404
from .models import Like, Club

@login_required
def like_club(request, club_name):
    club = get_object_or_404(Club, club_name=club_name)
    try:
        like, created = Like.objects.get_or_create(user=request.user, club=club)
        if created:
            message = 'You have successfully liked this club!'
        else:
            like.delete()
            message = 'You have successfully unliked this club!'
        return JsonResponse({'success': True, 'message': message})
    except Like.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Club not found'}, status=404)

@login_required
def user_profile(request):
    liked_clubs = Like.objects.filter(user=request.user).select_related('club')
    return render(request, 'hobby_clubs/user_profile.html', {'user': request.user, 'liked_clubs': liked_clubs})


from django.contrib.auth import views as auth_views

def custom_password_change(request):
    if request.method == 'POST':
        form = auth_views.PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()

            return redirect('user_profile') 
    else:
        form = auth_views.PasswordChangeForm(request.user)
    return render(request, 'hobby_clubs/password_change.html', {'form': form})

from django.urls import reverse
from django.http import HttpResponseRedirect

def my_view(request):
    # 重定向到 'password_change' 页面
    return HttpResponseRedirect(reverse('password_change'))

