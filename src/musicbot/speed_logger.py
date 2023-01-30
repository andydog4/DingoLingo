import time, logging


def timer(f):
    async def wrap(*args, **kwargs):
        time1 = time.perf_counter_ns()
        result = await f(*args, **kwargs)
        time2 = time.perf_counter_ns()
        logging.info(f'{f.__name__:s} function took {(time2-time1)/1000000.0:.4f} ms')
        return result
    return wrap