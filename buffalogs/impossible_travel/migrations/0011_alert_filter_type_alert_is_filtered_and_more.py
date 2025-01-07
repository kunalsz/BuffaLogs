# Generated by Django 4.2.16 on 2025-01-07 16:35

import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone
import impossible_travel.models
from impossible_travel.constants import AlertDetectionType
import logging

logger = logging.getLogger(__name__)


def update_alert_name(apps, schema_editor):
    Alert = apps.get_model("impossible_travel", "Alert")
    for alert in Alert.objects.all():
        if alert.name == "Impossible Travel detected":
            alert.name = AlertDetectionType.IMP_TRAVEL
        elif alert.name == "Login from new country":
            alert.name = AlertDetectionType.NEW_COUNTRY
        elif alert.name == "Login from new device":
            alert.name = AlertDetectionType.NEW_DEVICE
        else:
            logger.error(f"Impossible to update the alert.name of the alert with id {alert.id}")
        alert.save()


class Migration(migrations.Migration):

    dependencies = [
        (
            "impossible_travel",
            "0010_config_alert_max_days_config_distance_accepted_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(update_alert_name, migrations.RunPython.noop),
        migrations.AddField(
            model_name="alert",
            name="filter_type",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    blank=True,
                    choices=[
                        (
                            "ignored_users filter",
                            "Alert filtered because the user is ignored - the user is in the Config.ignored_users list or Config.enabled_users list is populated",
                        ),
                        (
                            "ignored_ips filter",
                            "Alert filtered because the IP is ignored - the ip is in the Config.ignored_ips list",
                        ),
                        (
                            "allowed_countries filter",
                            "Alert filtered because the country is whitelisted - the country is in the Config.allowed_countries list",
                        ),
                        (
                            "is_vip_filter",
                            "Alert filtered because the user is not vip - Config.alert_is_vip_only is True and the usre is not in the Config.vip_users list",
                        ),
                        (
                            "alert_minimum_risk_score filter",
                            "Alert filtered because the User.risk_score is lower than the threshold set in Config.alert_minimum_risk_score",
                        ),
                        (
                            "filtered_alerts_types filter",
                            "Alert filtered because this detection type is excluded - the Alert.name detection type is in the Config.filtered_alerts_types list",
                        ),
                        (
                            "ignore_mobile_logins filter",
                            "Alert filtered because the login is from a mobile device - Config.ignore_mobile_logins is True",
                        ),
                        (
                            "ignored_ISPs filter",
                            "Alert filtered because the ISP is whitelisted - The ISP is in the Config.ignored_ISPs list",
                        ),
                    ],
                    max_length=50,
                ),
                blank=True,
                default=list,
                help_text="List of filters that disabled the related alert",
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="alert",
            name="is_filtered",
            field=models.BooleanField(
                default=False,
                help_text="Show if the alert has been filtered because of some filter (listed in the filter_type field)",
            ),
        ),
        migrations.AddField(
            model_name="config",
            name="alert_is_vip_only",
            field=models.BooleanField(
                default=False,
                help_text="Flag to send alert only related to the users in the vip_users list",
            ),
        ),
        migrations.AddField(
            model_name="config",
            name="alert_minimum_risk_score",
            field=models.CharField(
                choices=[
                    ("No risk", "User has no risk"),
                    ("Low", "User has a low risk"),
                    ("Medium", "User has a medium risk"),
                    ("High", "User has a high risk"),
                ],
                default="No risk",
                help_text="Select the risk_score that users should have at least to send alert",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="config",
            name="enabled_users",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=impossible_travel.models.get_default_enabled_users,
                help_text="List of selected users on which the detection will perform",
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="config",
            name="filtered_alerts_types",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    blank=True,
                    choices=[
                        ("New Device", "Login from new device"),
                        ("Imp Travel", "Impossible Travel detected"),
                        ("New Country", "Login from new country"),
                        ("User Risk Threshold", "User risk higher than threshold"),
                        ("Login Anonymizer Ip", "Login from an anonymizer IP"),
                        (
                            "Atypical Country",
                            "Login from a country not visited recently",
                        ),
                    ],
                    max_length=50,
                ),
                blank=True,
                default=list,
                help_text="List of alerts' types to exclude from the alerting",
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="config",
            name="ignore_mobile_logins",
            field=models.BooleanField(
                default=False,
                help_text="Flag to ignore mobile devices from the detection",
            ),
        ),
        migrations.AddField(
            model_name="config",
            name="ignored_ISPs",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=impossible_travel.models.get_default_ignored_ISPs,
                help_text="List of ISPs names to remove from the detection",
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="alert",
            name="name",
            field=models.CharField(
                choices=[
                    ("New Device", "Login from new device"),
                    ("Imp Travel", "Impossible Travel detected"),
                    ("New Country", "Login from new country"),
                    ("User Risk Threshold", "User risk higher than threshold"),
                    ("Login Anonymizer Ip", "Login from an anonymizer IP"),
                    ("Atypical Country", "Login from a country not visited recently"),
                ],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="config",
            name="allowed_countries",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=20),
                blank=True,
                default=impossible_travel.models.get_default_allowed_countries,
                help_text="List of countries to exclude from the detection, because 'trusted' for the customer",
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="config",
            name="ignored_ips",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=impossible_travel.models.get_default_ignored_ips,
                help_text="List of IPs to remove from the detection",
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="config",
            name="ignored_users",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=impossible_travel.models.get_default_ignored_users,
                help_text="List of users to be ignored from the detection",
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="config",
            name="vip_users",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=impossible_travel.models.get_default_vip_users,
                help_text="List of users considered more sensitive",
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="login",
            name="timestamp",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="user",
            name="risk_score",
            field=models.CharField(
                choices=[
                    ("No risk", "User has no risk"),
                    ("Low", "User has a low risk"),
                    ("Medium", "User has a medium risk"),
                    ("High", "User has a high risk"),
                ],
                default="No risk",
                max_length=30,
            ),
        ),
        migrations.AddConstraint(
            model_name="alert",
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        "name__in",
                        [
                            "New Device",
                            "Imp Travel",
                            "New Country",
                            "User Risk Threshold",
                            "Login Anonymizer Ip",
                            "Atypical Country",
                        ],
                    )
                ),
                name="valid_alert_name_choice",
            ),
        ),
        migrations.AddConstraint(
            model_name="alert",
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        "filter_type__contained_by",
                        [
                            (
                                "ignored_users filter",
                                "Alert filtered because the user is ignored - the user is in the Config.ignored_users list or Config.enabled_users list is populated",
                            ),
                            (
                                "ignored_ips filter",
                                "Alert filtered because the IP is ignored - the ip is in the Config.ignored_ips list",
                            ),
                            (
                                "allowed_countries filter",
                                "Alert filtered because the country is whitelisted - the country is in the Config.allowed_countries list",
                            ),
                            (
                                "is_vip_filter",
                                "Alert filtered because the user is not vip - Config.alert_is_vip_only is True and the usre is not in the Config.vip_users list",
                            ),
                            (
                                "alert_minimum_risk_score filter",
                                "Alert filtered because the User.risk_score is lower than the threshold set in Config.alert_minimum_risk_score",
                            ),
                            (
                                "filtered_alerts_types filter",
                                "Alert filtered because this detection type is excluded - the Alert.name detection type is in the Config.filtered_alerts_types list",
                            ),
                            (
                                "ignore_mobile_logins filter",
                                "Alert filtered because the login is from a mobile device - Config.ignore_mobile_logins is True",
                            ),
                            (
                                "ignored_ISPs filter",
                                "Alert filtered because the ISP is whitelisted - The ISP is in the Config.ignored_ISPs list",
                            ),
                        ],
                    )
                ),
                name="valid_alert_filter_type_choices",
            ),
        ),
        migrations.AddConstraint(
            model_name="config",
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        "alert_minimum_risk_score__in",
                        ["No risk", "Low", "Medium", "High"],
                    )
                ),
                name="valid_config_alert_minimum_risk_score_choice",
            ),
        ),
        migrations.AddConstraint(
            model_name="config",
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        "filtered_alerts_types__contained_by",
                        [
                            (
                                "ignored_users filter",
                                "Alert filtered because the user is ignored - the user is in the Config.ignored_users list or Config.enabled_users list is populated",
                            ),
                            (
                                "ignored_ips filter",
                                "Alert filtered because the IP is ignored - the ip is in the Config.ignored_ips list",
                            ),
                            (
                                "allowed_countries filter",
                                "Alert filtered because the country is whitelisted - the country is in the Config.allowed_countries list",
                            ),
                            (
                                "is_vip_filter",
                                "Alert filtered because the user is not vip - Config.alert_is_vip_only is True and the usre is not in the Config.vip_users list",
                            ),
                            (
                                "alert_minimum_risk_score filter",
                                "Alert filtered because the User.risk_score is lower than the threshold set in Config.alert_minimum_risk_score",
                            ),
                            (
                                "filtered_alerts_types filter",
                                "Alert filtered because this detection type is excluded - the Alert.name detection type is in the Config.filtered_alerts_types list",
                            ),
                            (
                                "ignore_mobile_logins filter",
                                "Alert filtered because the login is from a mobile device - Config.ignore_mobile_logins is True",
                            ),
                            (
                                "ignored_ISPs filter",
                                "Alert filtered because the ISP is whitelisted - The ISP is in the Config.ignored_ISPs list",
                            ),
                        ],
                    )
                ),
                name="valid_alert_filters_choices",
            ),
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.CheckConstraint(
                check=models.Q(("risk_score__in", ["No risk", "Low", "Medium", "High"])),
                name="valid_user_risk_score_choice",
            ),
        ),
    ]
