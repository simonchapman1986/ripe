

# peform check to see if celery worker available
def get_celery_worker_status():
    """
    >>> get_celery_worker_status()
    True
    """
    import subprocess
    process = subprocess.Popen("ps auxx | grep celeryd", shell=True, stdout=subprocess.PIPE)
    count = len(process.stdout.readlines())
    if count > 2:
        # we have workers other than our grep statements
        return True
    # celery not running....
    return False