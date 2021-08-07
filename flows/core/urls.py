from django.urls import path

from . import views

urlpatterns = [
    path(
        "output/<str:execution_id>",
        views.WorkflowExecutionOutputAPI.as_view(),
    ),
    path("<str:workflow_id>/exec", views.WorkflowExecutionAPI.as_view()),
]
