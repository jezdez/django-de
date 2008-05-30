import markdown
from django import template
from django.template.defaultfilters import stringfilter, mark_safe, striptags, truncatewords

register = template.Library()
    
@register.filter
@stringfilter
def strip_jobdescription(content, max_words=None):
    content = striptags(content)
    if max_words and int(max_words) > 0:
        content = truncatewords(content, max_words)    
    content = markdown.markdown(content)
    return mark_safe(content)

@register.filter
@stringfilter
def obfuscate_email(email):
    email = email.replace("@", " <em>(at)</em> ")
    email = email.replace(".", " <em>(dot)</em> ")
    return mark_safe(email)
