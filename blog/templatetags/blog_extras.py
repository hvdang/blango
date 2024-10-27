from django import template
from django.contrib.auth.models import User
from django.utils.html import format_html
from blog.models import Post


register = template.Library()
    

@register.filter
def author_details(author, current_user):
    """filter with safe html using format_html
    To be safer and use less code, use the format_html function, 
    which escapes strings parameters before interpolation.
    Using format_html will automatically escape the text. Malicious code would not be executed."""
    if not isinstance(author, User):
        return ""
    
    if author == current_user:
        return format_html("<strong>me</strong>")
    
    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"
    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html('</a>')
    else:
        prefix = ""
        suffix = ""
        
    return format_html('{}{}{}', prefix, name, suffix)


@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
    return format_html("</div>")


@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)

@register.simple_tag
def endcol():
    return format_html('</div>')


@register.simple_tag(takes_context=True)
def author_details_tag(context):
    """_t can also have access to all the same context variables as the template in which it’s used.
    One example might be to always be able to access the request variable without having to remember to pass it into the template tag all the time.
    """
    request = context['request']
    current_user = request.user
    post = context['post']
    author = post.author
        
    if author == current_user:
        return format_html("<strong>me</strong>")
    
    if author.first_name and author.last_name:
        name = f'{author.first_name} {author.last_name}'
    else:
        name = f'{author.username}'
    
    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html('</a>')
    else:
        prefix = ''
        suffix = ''
    
    return format_html("{}{}{}", prefix, name, suffix)


@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    return {"title": "Recent Posts", "posts": posts}
