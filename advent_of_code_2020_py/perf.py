import time


def TimedMethod(f):
    def timed(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        end = time.perf_counter()
        print(f"{f.__name__} took {end - start} seconds")
        return result

    return timed
