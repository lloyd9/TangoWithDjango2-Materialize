from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserProfileForm
from datetime import datetime
from rango.bing_search import run_query, read_bing_key
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

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

class AboutView(View):
    def get(self, request):
        # Call the helper function visitor_cookie_handler
        visitor_cookie_handler(request)
        # Init context
        context_dict = {
            'my_name': 'Lloyd'
        }
        context_dict['visits'] = request.session['visits']
        return render(request,
                      'rango/about.html',
                      context_dict)
'''             
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
'''

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

    # Handle POST request from the search field
    result_list = []
    curr_query = ''
    if request.method == 'POST':
        query = request.POST['query'].strip()
        curr_query = query
        # Check if there's a query
        if query:
            result_list = run_query(query)
            context_dict['result_list'] = result_list
            context_dict['query'] = curr_query

    return render(request,
                  'rango/category.html',
                  context_dict)

class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm()
        form = CategoryForm(request.POST)
        # If form is valid, save form then return template
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
        return render(request, 'rango/add_category.html', {'form', form})


'''
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
'''

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

# def search(request):
#     result_list = []
#     # Get the current query, then display it in text/search field
#     curr_query = ''
#     if request.method == 'POST':
#         query = request.POST['query'].strip()
#         curr_query = query
#         if query:
#             # Get result of request
#             search_res = run_query(query)
#     # Init context
#     context_dict = {
#         'result_list': result_list,
#         'query': curr_query
#     }

#     return render(request,
#                   'rango/search.html',
#                   context_dict)

def goto_url(request):
    page_id = None
    # Redirect url if page is None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            try:
                page_id = request.GET['page_id']
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.save()
                url = page.url
                print(f'Views incremented, {page.views}. URL, {url}')
            except:
                pass
                print('Page not found')
        print(f'Redirecting url, {url}')
    return redirect(url)

@login_required
def register_profile(request):
    print('register_profile')
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('index')
        else:
            print(form.errors)
    # Init context
    context_dict = {'form': form}
    
    return render(request,
                  'rango/profile_registration.html',
                  context_dict)

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect('index')

        userprofile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})
        return (user, userprofile, form)
    
    @method_decorator(login_required)
    def get(self, request, username):
        (user, userprofile, form) = self.get_user_details(username)
        return render(request, 'rango/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})

    @method_decorator(login_required)
    def post(self, request, username):
        (user, userprofile, form) = self.get_user_details(username)
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)
        return render(request, 'rango/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})


@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()

    return render(request, 'rango/list_profiles.html', {'userprofile_list': userprofile_list})

@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        likes = 0
    if cat_id:
        cat = Category.objects.get(id=cat_id)
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)

def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list

def suggest_category(request):
    cat_list = []
    starts_with = ''

    if request.method == 'GET':
        # Get suggestion from AJAX
        starts_with = request.GET['suggestion']

    # First or top 8 matching results
    cat_list = get_category_list(8, starts_with)
    if len(cat_list) == 0:
        # Get category list in descending
        cat_list = Category.objects.order_by('-likes')
    return render(request, 'rango/cats.html', {'cats': cat_list})

@login_required
def auto_add_page(request):
    cat_id, url, title = None, None, None
    context_dict = {}
    # Parse data sent from AJAX
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            # Get or create new page with data from AJAX
            _ = Page.objects.get_or_create(category=category,
                                           title=title,
                                           url=url)
            #  Sort pages in specific category in descending order
            pages = Page.objects.filter(category=category).order_by('-views')
            context_dict['pages'] = pages
    return render(request, 'rango/page_list.html', context_dict)

# def register(request):
#     user_form = UserForm()
#     return render(request,
#                   'registration/registration_form.html',
#                   {'user_form': user_form})