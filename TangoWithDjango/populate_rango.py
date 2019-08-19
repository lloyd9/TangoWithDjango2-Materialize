import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    # Create data to be populated in DB
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/2/tutorial/'},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/'},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorials/python/'}
    ]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'http://docs.djangoproject.com/en/1.9/intro/tutorial01/'},
        {'title': 'Django Rocks',
         'url': 'http://www.djangorocks.com/'},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/'}
    ]

    other_pages = [
        {'title': 'Bottle',
         'url': 'http://www.bottlepy.org/docs/dev/'},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org'}
    ]

    # TODO: create data for likes and views for every category (Python, ...)
    # Then append it to cats dict then maybe alter the add cat method?

    cats = {
        'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
        'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
        'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16}
    }

    # Iterate key and val of cats dict, then add data to page and category
    for cat, cat_data in cats.items():
        # Pass the key and val to add_cat
        c = add_cat(cat, cat_data)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])
    
    # Print added data in category and page
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {str(c)} - {str(p)}')

# Add data to page method
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

# Add data to category method
def add_cat(name, cat_data):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = cat_data['views']
    c.likes = cat_data['likes']
    c.save()
    return c

# Start script
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()