import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
# from django.db.models import Avg  
# from django.http import HttpResponse

from .models import Club, Review, Rating
from .forms import ReviewForm, RatingForm

def index(request):
    """The home page for Hobby Log."""
    return render(request, 'hobby_clubs/index.html')


@login_required
def all_clubs(request):
    clubs = []
    with open('databasestore/clubs-info.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            clubs.append(row)
    return render(request, 'hobby_clubs/all_clubs.html', {'clubs': clubs})



from django.shortcuts import get_object_or_404

from django.http import HttpResponseBadRequest

@login_required
def club(request, unique_identifier):
    """Show a single club and all its reviews."""
    club = get_object_or_404(Club, unique_identifier=unique_identifier)
    reviews = club.reviews.order_by('-date_added')
    
    # Calculate the average rating
    club.calculate_average_rating()
    
    # Retrieve the user's rating for the club
    user_rating = Rating.objects.filter(club=club, user=request.user).first()
    
    context = {'club': club, 'reviews': reviews, 'user_rating': user_rating}
    return render(request, 'hobby_clubs/club.html', context)




@login_required
def new_review(request, unique_identifier):
    """Add a new review for a particular club."""
    club = get_object_or_404(Club, unique_identifier=unique_identifier)

    if request.method == 'POST':
        # POST data submitted; process data.
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.club = club
            new_review.save()
            messages.success(request, 'Your review has been added successfully!')
            return redirect('hobby_clubs:club', unique_identifier=unique_identifier)
    else:
        # No data submitted; create a blank form.
        form = ReviewForm()

    # Pass the club_id to the template.
    context = {'club': club, 'form': form}
    return render(request, 'hobby_clubs/new_review.html', context)

@login_required
def edit_review(request, review_id):
    """Edit an existing review."""
    review = get_object_or_404(Review, id=review_id)
    club = review.club

    if club.owner != request.user:
        raise Http404

    if request.method == 'POST':
        form = ReviewForm(instance=review, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated successfully!')
            return redirect('hobby_clubs:club', unique_identifier=club.unique_identifier)
    else:
        form = ReviewForm(instance=review)

    context = {'review': review, 'club': club, 'form': form }
    return render(request, 'hobby_clubs/edit_review.html', context)

# @login_required
# def rate_club(request, unique_identifier):
#     """Rate a particular club."""
#     club = get_object_or_404(Club, unique_identifier=unique_identifier)
#     user = request.user

#     if request.method == 'POST':
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             rating_value = form.cleaned_data['rating']
#             existing_rating = Rating.objects.filter(club=club, user=user).first()
#             if existing_rating:
#                 existing_rating.rating = rating_value
#                 existing_rating.save()
#                 messages.success(request, 'Your rating has been updated successfully!')
#             else:
#                 new_rating = Rating(club=club, user=user, rating=rating_value)
#                 new_rating.save()
#                 messages.success(request, 'Your rating has been added successfully!')
#             return redirect('hobby_clubs:club', unique_identifier=unique_identifier)
#     else:
#         form = RatingForm()

#     return render(request, 'hobby_clubs/rate_club.html', {'club': club, 'form': form})



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
        
        return render(request, 'hobby_clubs/search_results.html', {'matching_clubs': matching_clubs})

from django.contrib.auth import logout

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        print("用户已注销")
        return redirect('hobby_clubs:index')
    return redirect('hobby_clubs:index') 
    
