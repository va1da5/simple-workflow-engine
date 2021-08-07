from typing import Any, Mapping

from celery import chain
from django.conf import settings

from .models import Workflow, WorkflowExecution
from .tasks import execute_code_block


def start_workflow(workflow_uuid: str, variables: Mapping[str, Any]):
    workflow = Workflow.objects.get(uuid=workflow_uuid)

    entry_code_block = workflow.code_blocks.filter(name="start").first()

    workflow_execution = WorkflowExecution(workflow=workflow)
    context = {
        "variables": variables,
        "workflow_id": str(workflow.uuid),
        "execution_id": str(workflow_execution.uuid),
        "output": [],
        "steps": [],
    }

    results = execute_code_block.si(
        context, workflow_uuid, str(entry_code_block.uuid)
    ).delay()

    workflow_execution.results_id = results.id
    workflow_execution.save()
    return workflow_execution.uuid


def get_workflow_execution_output(workflow_execution_id: str):
    workflow_execution = WorkflowExecution.objects.get(uuid=workflow_execution_id)
    return workflow_execution.output
