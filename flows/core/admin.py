from django.contrib import admin

from flows.core.models import CodeBlock, Connector, Log, Workflow, WorkflowExecution


class LogAdmin(admin.ModelAdmin):
    readonly_fields = (
        "uuid",
        "workflow_execution",
        "code_block",
        "exception",
        "context",
        "created_at",
    )
    list_display = ("uuid", "workflow_execution", "code_block", "created_at")


class CodeBlockAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    list_display = (
        "uuid",
        "name",
        "workflow",
        "created_at",
        "updated_at",
        "enabled",
    )


class WorkflowAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    list_display = ("uuid", "name", "description", "created_at", "updated_at")


class WorkflowExecutionAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid", "workflow")
    list_display = ("uuid", "workflow", "created_at", "updated_at")


class ConnectorAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    list_display = (
        "uuid",
        "type",
        "left_code_block",
        "right_code_block",
        "created_at",
    )


admin.site.register(Log, LogAdmin)
admin.site.register(CodeBlock, CodeBlockAdmin)
admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(WorkflowExecution, WorkflowExecutionAdmin)
admin.site.register(Connector, ConnectorAdmin)
