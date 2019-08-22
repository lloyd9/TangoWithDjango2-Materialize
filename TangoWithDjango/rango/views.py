from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm
from datetime import datetime

# Create your views here.
def index(request):
    # # Test cookie
    # request.session.set_test_cookie()

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
    
    # Call the helper function visitor_cookie_handler
    visitor_cookie_handler(request)
    # Update context_dict, add visits
    context_dict['visits'] = request.session['visits']
    # Render the template
    return render(request,
                  'rango/index.html',
                  context_dict)
                  
def about(request):
    # # Test if cookie is received
    # if request.session.test_cookie_worked():
    #     print('TEST COOKIE WORKED!')
    #     request.session.delete_test_cookie()
    # print(request.user)

    # Call the helper functio visitor_cookie_handler
    visitor_cookie_handler(request)
    # Init context
    context_dict = {
        'my_name': 'Lloyd'
    }
    context_dict['visits'] = request.session['visits']
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

def add_category(request):
    form = CategoryForm()

    # POST Request
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # If form is valid, save form then return template
        if form.is_valid():
            cat = form.save(commit=True)
            # print(cat, cat.slug)
            return index(request)
        # Else, return built-in form errors
        else:
            print(form.errors)
    # Init context to be passed in the template
    context_dict = {
        'form': form
    }

    return render(request,
                  'rango/add_category.html',
                  context_dict)

def add_page(request, category_name_slug):
    try:
        # Get category slug
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        # Set to None if not exist
        category = None

    form = PageForm()

    # POST Request
    if request.method == 'POST':
        form = PageForm(request.POST)
        # If form is valid and category isn't empty, save form then return template
        if form.is_valid():
            if category:
                print(category, '- Category from add_page')
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            # Return form erors
            print(form.errors)
    
    # Init context to be passed in the template
    context_dict = {
        'form': form,
        'category': category
    }

    return render(request,
                  'rango/add_page.html',
                  context_dict)

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Get number of visits (this time in server-side), default 1 if none
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    # Get date of last visit
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    # Format last visit date
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    # Get the days of date today - date of last visit
    if (datetime.now() - last_visit_time).days > 0:
        # If days is greater than 1, increment visits then set the last visit to today
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        # Else, last visit will not change
        request.session['last_visit'] = last_visit_cookie
    # Update or set the number of visits (Since the use of this helper function is just to get the current number of visits)
    request.session['visits'] = visits

# def register(request):
#     user_form = UserForm()
#     return render(request,
#                   'registration/registration_form.html',
#                   {'user_form': user_form})