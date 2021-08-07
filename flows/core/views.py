from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services


class WorkflowExecutionAPI(APIView):
    def post(self, request, workflow_id):
        execution_id = services.start_workflow(workflow_id, request.data)
        return Response({"execution_id": execution_id})


class WorkflowExecutionOutputAPI(APIView):
    def get(self, request, execution_id):
        output = services.get_workflow_execution_output(execution_id)
        return Response(output)
