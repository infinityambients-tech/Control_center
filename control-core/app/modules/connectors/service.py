import requests
from sqlalchemy.orm import Session
from app.modules.projects import models, schemas
from datetime import datetime
from app.core.security import decrypt_secret
import logging

logger = logging.getLogger(__name__)

class ProjectConnector:
    def __init__(self, project: models.Project):
        self.project = project
        api_key = decrypt_secret(project.api_key_encrypted) if project.api_key_encrypted else ""
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def fetch_metrics(self):
        url = f"{self.project.api_base_url}/admin-sync/metrics"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch metrics for {self.project.name}: {e}")
            return None

    def fetch_subscriptions(self):
        url = f"{self.project.api_base_url}/admin-sync/subscriptions"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json() # Expecting a list of subs
        except Exception as e:
            logger.error(f"Failed to fetch subscriptions for {self.project.name}: {e}")
            return []

    def fetch_payments(self):
        url = f"{self.project.api_base_url}/admin-sync/payments"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json() # Expecting a list of payments
        except Exception as e:
            logger.error(f"Failed to fetch payments for {self.project.name}: {e}")
            return []

    def sync(self, db: Session):
        # 1. Sync Metrics
        metrics_data = self.fetch_metrics()
        if metrics_data:
            metric_in = schemas.MetricBase(
                date=datetime.utcnow(),
                mrr=metrics_data.get("mrr", 0.0),
                arr=metrics_data.get("arr", 0.0),
                active_subscriptions=metrics_data.get("active_subscriptions", 0),
                failed_payments=metrics_data.get("failed_payments", 0),
                revenue_today=metrics_data.get("revenue_today", 0.0)
            )
            crud.create_metric(db, metric_in, self.project.id)

        # 2. Sync Subscriptions Snapshots
        subs_data = self.fetch_subscriptions()
        for sub in subs_data:
            db_sub = models.SubscriptionSnapshot(
                project_id=self.project.id,
                external_id=sub.get("id"),
                plan=sub.get("plan"),
                status=sub.get("status"),
                current_period_end=datetime.fromisoformat(sub.get("current_period_end")) if sub.get("current_period_end") else None
            )
            db.add(db_sub)

        # 3. Sync Payments Snapshots
        payments_data = self.fetch_payments()
        for pay in payments_data:
            db_pay = models.PaymentSnapshot(
                project_id=self.project.id,
                external_payment_id=pay.get("id"),
                amount=pay.get("amount"),
                currency=pay.get("currency"),
                status=pay.get("status")
            )
            db.add(db_pay)

        db.commit()
        return True

def sync_all_projects(db: Session):
    projects = crud.get_projects(db)
    results = []
    for project in projects:
        connector = ProjectConnector(project)
        success = connector.sync(db)
        results.append({"project": project.name, "success": success})
    return results
