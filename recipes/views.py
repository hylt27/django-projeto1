from django.shortcuts import get_list_or_404, get_object_or_404, render
from utils.pagination import make_pagination
from .models import Recipe
from django.http import Http404
from django.db.models import Q

import os

from django.contrib import messages

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

def home(request):
    recipes = Recipe.objects.filter(
        is_published=True).order_by('-id')

    messages.error(request, 'Epa, você foi pesquisar algo que eu vi.')

    page_obj, pagination_range = make_pagination(
        request,
        queryset=recipes,
        per_page=PER_PAGE,
    )

    return render(
        request,
        'recipes/pages/home.html',
        context={
            'recipes': page_obj,
            'pagination_range': pagination_range})


def category(request, category_id):
    # view function for when one recipe category is opened

    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id,
        is_published=True).order_by('-id'))

    page_obj, pagination_range = make_pagination(
        request,
        queryset=recipes,
        per_page=PER_PAGE,
    )

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'Category | {recipes[0].category.name}'
    })


def recipe(request, id):
    # view function for when one recipe is opened

    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True
    })

def search(request):
    # view function to the search page

    search_term = request.GET.get('q', default='').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request,
        queryset=recipes,
        per_page=PER_PAGE,
    )

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}'
    })