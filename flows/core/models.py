import uuid

from django.db import models


class Workflow(models.Model):
    uuid = models.UUIDField(verbose_name="Workflow ID", unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, verbose_name="Workflow Name")
    description = models.CharField(max_length=500, verbose_name="Workflow Description")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f"<Workflow: {self.name}:{self.uuid}>"

    def __str__(self) -> str:
        return self.__repr__()


class CodeBlock(models.Model):
    uuid = models.UUIDField(
        verbose_name="CodeBlock ID", unique=True, default=uuid.uuid4
    )
    workflow = models.ForeignKey(
        Workflow, on_delete=models.CASCADE, related_name="code_blocks"
    )
    name = models.CharField(max_length=50, verbose_name="CodeBlock Name")
    description = models.CharField(
        max_length=500, verbose_name="Short Description", blank=True, null=True
    )
    code = models.TextField(verbose_name="CodeBlock Code")
    enabled = models.BooleanField(default=True, verbose_name="CodeBlock Enabled")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f"<CodeBlock: {self.name}:{self.uuid}>"

    def __str__(self) -> str:
        return self.__repr__()


class WorkflowExecution(models.Model):
    uuid = models.UUIDField(
        verbose_name="Workflow Execution ID", unique=True, default=uuid.uuid4
    )
    workflow = models.ForeignKey(
        Workflow, on_delete=models.CASCADE, related_name="executions"
    )

    # results_id = models.UUIDField(verbose_name="Execution Results ID", unique=True)

    output = models.JSONField(verbose_name="Output", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f"<WorkflowExecution: {self.workflow.name}:{self.created_at}>"

    def __str__(self) -> str:
        return self.__repr__()


class Connector(models.Model):

    uuid = models.UUIDField(
        verbose_name="Connector ID", unique=True, default=uuid.uuid4
    )

    CONNECTOR_TYPES = [
        ("SUCCESS", "Successful Execution"),
        ("FAILURE", "Failed Execution"),
    ]

    type = models.CharField(
        max_length=8,
        choices=CONNECTOR_TYPES,
        default="SUCCESS",
        verbose_name="Connector Type",
    )

    left_code_block = models.ForeignKey(
        CodeBlock, on_delete=models.CASCADE, related_name="outgoing_connectors"
    )
    right_code_block = models.ForeignKey(
        CodeBlock, on_delete=models.CASCADE, related_name="incoming_connectors"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return (
            f"<Connector: {self.type} ({self.left_code_block}:{self.right_code_block})>"
        )

    def __str__(self) -> str:
        return self.__repr__()


class Log(models.Model):
    uuid = models.UUIDField(verbose_name="Log ID", unique=True, default=uuid.uuid4)
    workflow_execution = models.ForeignKey(
        WorkflowExecution, on_delete=models.CASCADE, related_name="logs"
    )
    code_block = models.ForeignKey(
        CodeBlock, on_delete=models.CASCADE, related_name="logs"
    )

    context = models.JSONField(verbose_name="Execution Context", blank=True, null=True)
    exception = models.TextField(verbose_name="Exception", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f"<ExecutionLog: {self.workflow_execution.workflow.name}:{self.code_block.name}:{self.uuid}>"

    def __str__(self) -> str:
        return self.__repr__()
