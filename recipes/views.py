from django.shortcuts import get_list_or_404, get_object_or_404, render
from .models import Recipe
from django.http import Http404
from django.db.models import Q


def home(request):
    # view function for the Home page

    recipes = Recipe.objects.filter(
        is_published=True).order_by('-id')

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    # view function for when one recipe category is opened

    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id,
                                                    is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
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

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': recipes,
    })