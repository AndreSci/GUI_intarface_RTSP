import datetime


def ShowWorkSpeed(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        original_result = func(*args, **kwargs)
        print(f"Time to work: {(datetime.datetime.now() - start).total_seconds()}")
        return original_result

    return wrapper
