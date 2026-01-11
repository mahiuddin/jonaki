# analytics/views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .utils import metabase_dashboard_embed_url

@staff_member_required
def analytics_dashboard(request):
    embed_url = metabase_dashboard_embed_url(dashboard_id=3)
    return render(request, "admin/metabase_dashboard.html", {
        "embed_url": embed_url
    })