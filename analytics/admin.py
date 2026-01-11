# analytics/admin.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .utils import metabase_dashboard_embed_url


class AnalyticsAdmin(admin.AdminSite):
    site_header = "Jonaki Inventory Admin"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "analytics/",
                self.admin_view(self.analytics_dashboard),
                name="analytics-dashboard",
            ),
        ]
        return custom_urls + urls

    def analytics_dashboard(self, request):
        embed_url = metabase_dashboard_embed_url(dashboard_id=5)
        return render(request, "admin/metabase_dashboard.html", {
            "embed_url": embed_url
        })
