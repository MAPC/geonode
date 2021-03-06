from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils import simplejson as json

from models import Story
from masshealth.places.models import Place
from masshealth.places.views import InOtherPlace

from geonode.utils import default_map_config
from geonode.maps.views import _resolve_map, _PERMISSION_MSG_VIEW

def story(request, place_slug, story_slug=None):
    page_type = "story"
    place = get_object_or_404(Place, slug=place_slug)

    place_stories = place.datastories.all()

    # Maybe return an alternate rendering if place_stories.count == 0?

    try:
        if story_slug is None:
            story = place_stories[0]
        else:
            story = place_stories.get(slug=story_slug)
    except (Story.DoesNotExist, IndexError):
        story = None

    if story:
        pages = story.pages.order_by('storypage__page_number')
    else:
        pages = []

    paginator = Paginator(pages, 1)

    page_count = paginator.num_pages

    page_num = request.GET.get('page_num')
    try:
        pgpg = paginator.page(page_num)
    except PageNotAnInteger:
        pgpg = paginator.page(1)
    except EmptyPage:
        pgpg = paginator.page(page_count)

    if not pgpg.object_list:
        # No pages
        page = None
        page_num = 0
        page_next = 0
        page_prev = 0
        page_count = 0
        config = default_map_config()[0]

    else:
        page = pgpg.object_list[0]
        page_num = pgpg.number
        page_next = pgpg.next_page_number() if pgpg.has_next() else 0
        page_prev = pgpg.previous_page_number() if pgpg.has_previous() else 0

        # map config
        if page.map is None:
            config = default_map_config()[0]
        else:
            map_obj = _resolve_map(request, page.map.id, 'maps.view_map', _PERMISSION_MSG_VIEW)
            config = map_obj.viewer_json()

    if story:
        spp = InOtherPlace.get_split('story', 'XXX', 'XXX', story.slug)
    else:
        spp = InOtherPlace.get_split('story', 'XXX', 'XXX')


    return render_to_response(
        'datastories/story.html',
        dict(story=story,
             page_type=page_type,
             page=page,
             page_num=page_num,
             page_count=page_count,
             page_prev=page_prev,
             page_next=page_next,
             paginator=paginator,
             paginator_page=pgpg,
             place=place,
             datastories=place_stories,
             same_place_parts=spp,
             WEAVE_URL=settings.WEAVE_URL,
             config = json.dumps(config),
             ),
        context_instance=RequestContext(request))

InOtherPlace(story, 'XXX')
InOtherPlace(story, 'XXX', 'YYY')
