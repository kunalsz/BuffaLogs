try:
    import requests
except ImportError:
    pass
from django.db.models import Q
from impossible_travel.alerting.base_alerting import BaseAlerting
from impossible_travel.models import Alert


class SlackAlerting(BaseAlerting):
    """
    Concrete implementation of the BaseQuery class for SlackAlerting.
    """

    def __init__(self, alert_config: dict):
        """
        Constructor for the Slack Alerter query object.
        """
        super().__init__()
        self.webhook_url = alert_config.get("webhook_url")

        if not self.webhook_url:
            self.logger.error("Slack Alerter configuration is missing required fields.")
            raise ValueError("Slack Alerter configuration is missing required fields.")

    def notify_alerts(self):
        """
        Execute the alerter operation.
        """
        alerts = Alert.objects.filter(Q(notified_status__slack=False) | ~Q(notified_status__has_key="slack"))

        for alert in alerts:
            alert_title, alert_description = self.alert_message_formatter(alert)
            alert_msg = {
                "attachments": [
                    {
                        "title": alert_title,
                        "text": alert_description,
                        "color": "#ff0000",
                    }
                ]
            }
            try:
                resp = requests.post(self.webhook_url, json=alert_msg, headers={"Content-Type": "application/json"})
                resp.raise_for_status()
                self.logger.info(f"Slack alert sent: {alert.name}")
                alert.notified_status["slack"] = True
                alert.save()
            except requests.RequestException as e:
                self.logger.exception(f"Slack alert failed for {alert.name}: {str(e)}")
