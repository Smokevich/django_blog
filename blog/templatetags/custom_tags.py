# from django import template

# register = template.Library()

# @register.filter
# def avatar_compile(link):
#     if link != 'images/user.png':
#         return link
#     return '../static/images/user.png'



# create the register instance by initializing it with the Library instance.
from django import template

register = template.Library()

# An upper function that capitalizes word passed to it. We then register the filter using a suitable name.
@register.filter
def get_avatar(link_image:str) -> str:
    if link_image == '':
      return '/static/images/user.png'
    return link_image.url


@register.filter
def fix_error_type(type:str) -> str:
   if type == 'error':
      return 'danger'
   return type

@register.filter(is_safe = False)
def pluralize(value, forms):
    """
    Подбирает окончание существительному после числа
    {{someval|pluralize:"товар,товара,товаров"}}
    """
    try:
        one, two, many = forms.split(u',')
        value = str(value)[-2:]  # 314 -> 14
        
        if (21 > int(value) > 4):
            return many
        
        if value.endswith('1'):
            return one
        elif value.endswith(('2', '3', '4')):
            return two
        else:
            return many

    except (ValueError, TypeError):
        return ''