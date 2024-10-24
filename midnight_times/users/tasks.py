from celery import shared_task

from .models import User, SearchResult
from celery import Celery


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


app = Celery("midnight_times")


@app.task
def clear_results():
    search_result = SearchResult.objects.all()
    search_result.update(articles_list=None)
