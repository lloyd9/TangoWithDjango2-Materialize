from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {
        'cats': Category.objects.all(),
        'act_cat': cat
    }

@register.filter
def does_exists(pages, result_key):
    # Return true if result title does exists in pages
    return pages.filter(title=result_key).exists()