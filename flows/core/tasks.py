import functools
import importlib
from typing import Any, Callable, Mapping

from celery import Task, shared_task
from django.conf import settings

from . import models


def import_workflow_step(workflow_id, code_block_id):
    path = f"{settings.WORKFLOWS_DIR}.{workflow_id}.{code_block_id}"
    module = importlib.__import__(path, fromlist=[None])
    importlib.reload(module)
    return module


def log_workflow_code_block_execution(code_block_id, context, exception=None):
    workflow_execution = models.WorkflowExecution.objects.get(
        uuid=context["execution_id"]
    )
    code_block = workflow_execution.workflow.code_blocks.get(
        uuid=code_block_id, enabled=True
    )
    models.Log(
        workflow_execution=workflow_execution,
        code_block=code_block,
        context=context,
        exception=str(exception),
    ).save()


def save_execution_output(execution_id, output):
    workflow_execution = models.WorkflowExecution.objects.get(uuid=execution_id)

    workflow_execution.output = output
    workflow_execution.save()


def decorate_step(func: Callable):
    @functools.wraps(func)
    def wrapper(context: Mapping[str, Any], task: Task, code_block_id: str):
        try:
            output = func(task=task, **context, _context_=context)
            context["output"].append(output)
            context["steps"].append(code_block_id)
            return context
        except Exception as e:
            raise e

    return wrapper


def get_next_code_block_id(current_code_block_id: str, type="SUCCESS"):
    code_block = models.CodeBlock.objects.get(uuid=current_code_block_id)
    connector = code_block.outgoing_connectors.filter(type=type).first()
    if connector:
        return str(connector.right_code_block.uuid)


class WorkflowTask(Task):
    pass


@shared_task(base=WorkflowTask, bind=True)
def execute_code_block(self, context, workflow_id, code_block_id):
    log_workflow_code_block_execution(code_block_id, context)
    module = import_workflow_step(workflow_id, code_block_id)
    try:
        context = decorate_step(module.handle)(
            context, task=self, code_block_id=code_block_id
        )

        if next_code_block_id := get_next_code_block_id(code_block_id):
            self.delay(context, workflow_id, next_code_block_id)
            return context

        return final.delay(context)

    except Exception as e:
        log_workflow_code_block_execution(code_block_id, context, e)
        if next_code_block_id := get_next_code_block_id(code_block_id, type="FAILURE"):
            self.delay(context, workflow_id, next_code_block_id)
            return context
        raise e


@shared_task(base=WorkflowTask)
def final(context):
    save_execution_output(context["execution_id"], context["output"][-1])
    return context
