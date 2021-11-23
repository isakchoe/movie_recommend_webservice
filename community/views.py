from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.core.paginator import Paginator
from movies.models import Movie


@require_GET
def index(request):
    reviews = Review.objects.order_by('-pk')
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'community/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create_review(request, movie_id):
    movie = get_object_or_404(Movie, movie_api_id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('community:detail_review', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/form.html', context)


@require_GET
def detail_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'community/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def update_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail_review', review.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'review': review,
        'form': form,
    }
    return render(request, 'community/form.html', context)


@require_POST
def delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user.is_authenticated:
        if request.user == review.user:
            review.delete()
            return redirect('community:index')
        return redirect('community:detail_review')


@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('community:detail_review', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/detail.html', context)


@require_POST
def delete_comment(request, review_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail_review', review_pk)


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail_review', article_pk)
