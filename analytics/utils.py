# analytics/utils.py

import jwt
import time
from django.conf import settings


def metabase_dashboard_embed_url(dashboard_id, params=None):
    payload = {
        "resource": {"dashboard": dashboard_id},
        "params": params or {},
        "exp": round(time.time()) + (60 * 60),  # 1 hour
    }

    token = jwt.encode(payload, settings.METABASE_SECRET_KEY, algorithm="HS256")

    return f"{settings.METABASE_SITE_URL}/embed/dashboard/{token}#bordered=true&titled=true"
