from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

# Create your views here.
def index(request):
    # Get top 5 of likes in '-' descending order
    category_list = Category.objects.order_by('-likes')[:5]
    # Get top 5 most viewed page
    page_list = Page.objects.order_by('-views')[:5]
    # Init context
    context_dict = {
        'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!",
        'categories': category_list,
        'pages': page_list
    }
    # Render page
    return render(request,
                  'rango/index.html',
                  context_dict)
                  
def about(request):
    # Init context
    context_dict = {
        'my_name': 'Lloyd'
    }
    # Render page
    return render(request,
                  'rango/about.html',
                  context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        # Get category_name_slug if exist, if not it'll raise a DoesNotExist exception
        category = Category.objects.get(slug=category_name_slug)
        # Return a filtered list of objects or an empty list
        pages = Page.objects.filter(category=category)
        # Set or append data to context dict
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        # Do nothing if not exist, the template will display 'no category' message
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request,
                  'rango/category.html',
                  context_dict)