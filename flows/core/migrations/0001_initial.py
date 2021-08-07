# Generated by Django 3.2.6 on 2021-08-07 15:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='CodeBlock ID')),
                ('name', models.CharField(max_length=50, verbose_name='CodeBlock Name')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Short Description')),
                ('code', models.TextField(verbose_name='CodeBlock Code')),
                ('enabled', models.BooleanField(default=True, verbose_name='CodeBlock Enabled')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='Workflow ID')),
                ('name', models.CharField(max_length=50, verbose_name='Workflow Name')),
                ('description', models.CharField(max_length=500, verbose_name='Workflow Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='Workflow Execution ID')),
                ('results_id', models.UUIDField(unique=True, verbose_name='Execution Results ID')),
                ('output', models.JSONField(blank=True, null=True, verbose_name='Output')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executions', to='core.workflow')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='Log ID')),
                ('context', models.JSONField(blank=True, null=True, verbose_name='Execution Context')),
                ('exception', models.TextField(blank=True, null=True, verbose_name='Exception')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='core.codeblock')),
                ('workflow_execution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='core.workflowexecution')),
            ],
        ),
        migrations.CreateModel(
            name='Connector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='Connector ID')),
                ('type', models.CharField(choices=[('SUCCESS', 'Successful Execution'), ('FAILURE', 'Failed Execution')], default='SUCCESS', max_length=8, verbose_name='Connector Type')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('left_code_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_connectors', to='core.codeblock')),
                ('right_code_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_connectors', to='core.codeblock')),
            ],
        ),
        migrations.AddField(
            model_name='codeblock',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_blocks', to='core.workflow'),
        ),
    ]