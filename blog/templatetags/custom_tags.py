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
def get_avatar(link_image):
    if link_image == '':
      return '/static/images/user.png'
    return link_image.url
