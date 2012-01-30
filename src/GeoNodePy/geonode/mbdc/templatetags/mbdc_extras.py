import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.contrib.auth.models import User

from django.conf import settings

from geonode.mbdc.models import Page, Topic
from geonode.snapshots.models import Regiontype
from geonode.weave.models import Visualization

from geonode.weave.utils import get_readable_vis

register = template.Library()


@register.inclusion_tag('mbdc/_header_about.html')
def get_header_about():

	about_pages = Page.objects.filter(section='about')

	return locals()

@register.inclusion_tag('mbdc/_header_primarynav.html')
def get_header_primarynav():

    snapshot_types = Regiontype.objects.all()
    resources_pages = Page.objects.filter(section='resources')
    community_pages = Page.objects.filter(section='community')

    return locals()

@register.inclusion_tag('mbdc/_footer.html', takes_context=True)
def get_footer(context):

    about_pages = Page.objects.filter(section='about')	
    resources_pages = Page.objects.filter(section='resources')
    community_pages = Page.objects.filter(section='community')
    legal_pages = Page.objects.filter(section='legal')
    snapshot_types = Regiontype.objects.all()
    topics = Topic.objects.all()
    STATIC_URL = context['STATIC_URL']

    return locals()

@register.inclusion_tag('mbdc/_data_search_bar.html', takes_context=True)
def get_data_search_bar(context):

    topics = Topic.objects.all()
    STATIC_URL = context['STATIC_URL']

    return locals()


@register.inclusion_tag('mbdc/_user_gallery.html', takes_context=True)
def get_user_gallery(context, request, user):

    try:
        readable_vis = get_readable_vis(request.user)
        visualizations = Visualization.objects.filter(owner=user, id__in=readable_vis)
    except:
        visualizations = Visualization.objects.none()

    nr_results = len(visualizations)
    MEDIA_URL = context['MEDIA_URL']

    return locals()


@register.filter()
def obfuscate(email, linktext=None, autoescape=None):
    """

    http://djangosnippets.org/snippets/1475/

    Given a string representing an email address,
    returns a mailto link with rot13 JavaScript obfuscation.
    
    Accepts an optional argument to use as the link text;
    otherwise uses the email address itself.
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    email = re.sub('@','\\\\100', re.sub('\.', '\\\\056', \
        esc(email))).encode('rot13')

    if linktext:
        linktext = esc(linktext).encode('rot13')
    else:
        linktext = email

    rotten_link = """<script type="text/javascript">document.write \
        ("<n uers=\\\"znvygb:%s\\\">%s<\\057n>".replace(/[a-zA-Z]/g, \
        function(c){return String.fromCharCode((c<="Z"?90:122)>=\
        (c=c.charCodeAt(0)+13)?c:c-26);}));</script>""" % (email, linktext)
    return mark_safe(rotten_link)
obfuscate.needs_autoescape = True