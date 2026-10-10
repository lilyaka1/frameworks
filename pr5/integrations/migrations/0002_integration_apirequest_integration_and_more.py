from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("integrations", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Integration",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("api_url", models.URLField()),
                ("key_configured", models.BooleanField(default=False)),
                ("service", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="integrations", to="integrations.service")),
            ],
            options={"ordering": ["service__name"], "constraints": [models.UniqueConstraint(fields=("service", "api_url"), name="unique_service_api_url")]},
        ),
        migrations.AddField(model_name="apirequest", name="integration", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="api_requests", to="integrations.integration")),
        migrations.AddField(model_name="apirequest", name="endpoint", field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name="apirequest", name="duration_ms", field=models.FloatField(default=0)),
    ]