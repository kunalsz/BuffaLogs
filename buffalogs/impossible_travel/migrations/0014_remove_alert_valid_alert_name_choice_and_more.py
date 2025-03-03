# Generated by Django 4.2.16 on 2025-03-03 07:57

import django.contrib.postgres.fields
from django.db import migrations, models
import impossible_travel.models
import impossible_travel.validators


class Migration(migrations.Migration):

    dependencies = [
        ("impossible_travel", "0013_alert_notified"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="alert",
            name="valid_alert_name_choice",
        ),
        migrations.RemoveConstraint(
            model_name="config",
            name="valid_alert_filters_choices",
        ),
        migrations.AddField(
            model_name="config",
            name="atypical_country_days",
            field=models.PositiveIntegerField(
                default=30,
                help_text="Days after which a login from a country is considered atypical",
            ),
        ),
        migrations.AddField(
            model_name="config",
            name="threshold_user_risk_alert",
            field=models.CharField(
                choices=[
                    ("No risk", "User has no risk"),
                    ("Low", "User has a low risk"),
                    ("Medium", "User has a medium risk"),
                    ("High", "User has a high risk"),
                ],
                default="No risk",
                help_text="Select the risk_score that a user should overcome to send the 'USER_RISK_THRESHOLD' alert",
                max_length=30,
            ),
        ),
        migrations.AlterField(
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
                            "Alert filtered because the user is not vip - Config.alert_is_vip_only is True and the user is not in the Config.vip_users list",
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
        migrations.AlterField(
            model_name="alert",
            name="name",
            field=models.CharField(
                choices=[
                    ("New Device", "Login from new device"),
                    ("Imp Travel", "Impossible Travel detected"),
                    ("New Country", "Login from new country"),
                    ("User Risk Threshold", "User risk_score increased"),
                    ("Anonymous IP Login", "Login from an anonymous IP"),
                    ("Atypical Country", "Login from an atypical country"),
                ],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="config",
            name="alert_max_days",
            field=models.PositiveIntegerField(
                default=45,
                help_text="Days after which the alerts will be removed from the db",
            ),
        ),
        migrations.AlterField(
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
                help_text="Select the risk_score that users should have at least to send the alerts",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="config",
            name="enabled_users",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=impossible_travel.models.get_default_enabled_users,
                help_text="List of selected users (strings or regex patterns) on which the detection will perform",
                null=True,
                size=None,
                validators=[impossible_travel.validators.validate_string_or_regex],
            ),
        ),
        migrations.AlterField(
            model_name="config",
            name="filtered_alerts_types",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    blank=True,
                    choices=[
                        ("New Device", "Login from new device"),
                        ("Imp Travel", "Impossible Travel detected"),
                        ("New Country", "Login from new country"),
                        ("User Risk Threshold", "User risk_score increased"),
                        ("Anonymous IP Login", "Login from an anonymous IP"),
                        ("Atypical Country", "Login from an atypical country"),
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
        migrations.AlterField(
            model_name="config",
            name="ip_max_days",
            field=models.PositiveIntegerField(
                default=45,
                help_text="Days after which the IPs will be removed from the db",
            ),
        ),
        migrations.AlterField(
            model_name="config",
            name="login_max_days",
            field=models.PositiveIntegerField(
                default=45,
                help_text="Days after which the logins will be removed from the db",
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
                            "Anonymous IP Login",
                            "Atypical Country",
                        ],
                    )
                ),
                name="valid_alert_name_choice",
            ),
        ),
        migrations.AddConstraint(
            model_name="config",
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        "filtered_alerts_types__contained_by",
                        [
                            "New Device",
                            "Imp Travel",
                            "New Country",
                            "User Risk Threshold",
                            "Anonymous IP Login",
                            "Atypical Country",
                        ],
                    ),
                    ("filtered_alerts_types__isnull", True),
                    _connector="OR",
                ),
                name="valid_alert_filters_choices",
            ),
        ),
    ]
