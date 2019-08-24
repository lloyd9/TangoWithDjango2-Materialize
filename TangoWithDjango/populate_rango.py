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
         'url': 'http://docs.python.org/2/tutorial/',
         'views': 42},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/',
         'views': 23},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorials/python/',
         'views': 63}
    ]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'http://docs.djangoproject.com/en/1.9/intro/tutorial01/',
         'views': 10},
        {'title': 'Django Rocks',
         'url': 'http://www.djangorocks.com/',
         'views': 22},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/',
         'views': 32}
    ]

    other_pages = [
        {'title': 'Bottle',
         'url': 'http://www.bottlepy.org/docs/dev/',
         'views': 12},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org',
         'views': 20}
    ]

    pascal_pages = [
        {
            'title': 'Pascal (programming language)',
            'url': 'https://en.wikipedia.org/wiki/Pascal_(programming_language)',
            'views': 1
        },
        {
            'title': 'Pascal Siakam',
            'url': 'https://en.wikipedia.org/wiki/Pascal_Siakam',
            'views': 67
        }
    ]

    perl_pages = [
        {
            'title': 'Perl',
            'url': 'https://www.perl.org/',
            'views': 168
        }
    ]

    php_pages = [
        {
            'title': 'PHP',
            'url': 'https://www.php.net/',
            'views': 8
        }
    ]

    prolog_pages = [
        {
            'title': 'Prolog',
            'url': 'https://en.wikipedia.org/wiki/Prolog',
            'views': 38
        }
    ]

    postscript_pages = [
        {
            'title': 'PostScript',
            'url': 'https://en.wikipedia.org/wiki/PostScript',
            'views': 58
        }
    ]

    programming_pages = [
        {
            'title': 'Programming',
            'url': 'https://en.wikipedia.org/wiki/Computer_programming',
            'views': 200
        }
    ]

    cats = {
        'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
        'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
        'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16},
        'Pascal': {'pages': pascal_pages, 'views': 68, 'likes': 102},
        'Perl': {'pages': perl_pages, 'views': 168, 'likes': 12},
        'PHP': {'pages': php_pages, 'views': 8, 'likes': 10},
        'Prolog': {'pages': prolog_pages, 'views': 38, 'likes': 22},
        'PostScript': {'pages': postscript_pages, 'views': 58, 'likes': 123},
        'Programming': {'pages': programming_pages, 'views': 200, 'likes': 196}
    }

    # Iterate key and val of cats dict, then add data to page and category
    for cat, cat_data in cats.items():
        # Pass the key and val to add_cat
        c = add_cat(cat, cat_data)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])
    
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