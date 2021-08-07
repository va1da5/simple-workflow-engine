import os
import shutil

from django.conf import settings
from django.db.models.signals import post_delete, post_save

from .models import CodeBlock, Workflow


def get_workflow_directory(workflow: Workflow):
    return os.path.join(settings.BASE_DIR, settings.WORKFLOWS_DIR, str(workflow.uuid))


def create_workflow_container(sender, instance: Workflow, **kwargs):
    workflow_dir = get_workflow_directory(instance)
    try:
        os.mkdir(workflow_dir)
        open(os.path.join(workflow_dir, "__init__.py"), "a").close()
    except FileExistsError:
        pass


def create_start_codeblock(sender, instance: Workflow, **kwargs):

    code = """def handle(**kwargs):
    return None"""

    if instance.code_blocks.count():
        return

    CodeBlock(
        workflow=instance,
        name="start",
        description="Auto-generated codeblock which gets executed first",
        code=code,
    ).save()


def delete_workflow_container(sender, instance: Workflow, **kwargs):
    workflow_dir = get_workflow_directory(instance)

    try:
        shutil.rmtree(workflow_dir)
    except OSError as e:
        print("Error: %s : %s" % (workflow_dir, e.strerror))


def create_code_block(sender, instance: CodeBlock, **kwargs):
    workflow_dir = get_workflow_directory(instance.workflow)
    with open(os.path.join(workflow_dir, f"{instance.uuid}.py"), "w") as f:
        f.write(instance.code)


def delete_code_block(sender, instance: CodeBlock, **kwargs):
    workflow_dir = get_workflow_directory(instance.workflow)
    os.remove(os.path.join(workflow_dir, f"{instance.uuid}.py"))


post_save.connect(create_workflow_container, sender=Workflow)
post_save.connect(create_start_codeblock, sender=Workflow)
post_delete.connect(delete_workflow_container, sender=Workflow)
post_save.connect(create_code_block, sender=CodeBlock)
post_delete.connect(delete_code_block, sender=CodeBlock)
