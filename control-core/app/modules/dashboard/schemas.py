from __future__ import annotations

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    projects_count: int
    active_subscriptions_count: int
    monthly_revenue_gross: float
    recent_deployments: list[dict] = []
    recent_activity: list[dict] = []

