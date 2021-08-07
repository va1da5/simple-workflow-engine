# Workflow Engine

This is a toy project, an attempt to create a simple workflow engine that could be easily scaled using [Celery](https://docs.celeryproject.org/en/stable/index.html).

## Components

 - [ ] Decision block (if/else)
 - [ ] Workflow
 - [ ] Logging Block
 - [ ] Idle/wait Block
 - [ ] ...


## Workflow Step Example 

The executor uses `handle` function to run code, so this name must be defined in the code block.

```python
import requests

def handle(variables=None, **kwargs):
    url = variables["url"]
    resp = requests.get(url)
    return resp.json()
```

## References

- [Introduction to Django Signals](https://www.pluralsight.com/guides/introduction-to-django-signals)
- [Where should signal handlers live in a django project?](https://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project)
- [Auto-reload Celery on code changes](https://www.distributedpython.com/2019/04/23/celery-reload/)
- [Selinon - An advanced task flow management on top of Celery](https://github.com/selinon/selinon)
