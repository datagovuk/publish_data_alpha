import os
import json

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render
from django.conf import settings
from django.utils.translation import ugettext as _

from datasets.logic import dataset_list, organisations_for_user
from tasks.logic import get_tasks_for_user
from stats.logic import get_stats
from runtime_config.logic import get_config

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard'))

    return render(request, "home.html", {})


@login_required()
def dashboard(request):
    tasks = get_tasks_for_user(request.user)
    organisations = organisations_for_user(request.user)

    # Use an actual organisation for this user
    stats = get_stats("cabinet-office", _("Downloads"))

    return render(request, "dashboard.html", {
        "orgs": json.dumps([str(o.id) for o in organisations]),
        "api_endpoint": os.environ.get('FIND_URL') or '',
        "tasks": tasks,
        "stats": stats
    })


@login_required()
def manage_data(request):
    q = request.GET.get('q')
    result = request.GET.get('result')
    sort = request.GET.get('sort')

    page = 1
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1


    if sort == 'name':
        sort_name_next = '-name'
        sort_published_next = 'published'
    elif sort == 'published':
        sort_name_next = 'name'
        sort_published_next = '-published'
    else:
        sort_name_next = 'name'
        sort_published_next = 'published'

    if sort and not sort in ['name', 'published', '-name', '-published']:
        sort = None

    total, page_count, datasets = dataset_list(
        request.user, page, filter_query=q, sort=sort
    )

    ckan_host = get_config('ckan.host') or ''

    return render(request, "manage.html", {
        "datasets": datasets,
        "total": total,
        "page_range": range(1, page_count),
        "current_page": page,
        "q": q or "",
        "result": result or "",
        "find_url": settings.FIND_URL or ckan_host,
        "sort": sort,
        "sort_name_next": sort_name_next,
        "sort_published_next": sort_published_next
    })
