from tasks.models import Task, UserHiddenTask, TASK_CATEGORIES
from ckan_proxy.logic import organization_list_for_user

def get_tasks_for_user(user):
    """ For the given user, find the tasks that
        they have in each category based on:
            * Their organisation membership
            * Them having the required permissions
            * Them not having skipped it before.
    """
    orgs = [o['name'] for o in organization_list_for_user(user)]
    user_permissions = [""]
    ignored_task_ids = UserHiddenTask.objects.values_list('task__id', flat=True)
    task_objs = Task.objects\
        .filter(owning_organisation__in=orgs)\
        .filter(required_permission_name__in=user_permissions)\
        .exclude(id__in=ignored_task_ids)\
        .all()

    tasks = {}
    for entry in TASK_CATEGORIES:
        tasks[entry[0]] = [t for t in task_objs if t.category == entry[0]]

    return tasks

def user_ignore_task(user, task):
    UserHiddenTask.objects.create(user=user, task=task)