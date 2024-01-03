import time, logging, cProfile
from pstats  import Stats


def timer(f):
    async def wrap(*args, **kwargs):
        time1 = time.perf_counter_ns()
        result = await f(*args, **kwargs)
        time2 = time.perf_counter_ns()
        logging.info(f'{f.__name__:s} function took {(time2-time1)/1000000.0:.4f} ms')
        return result
    return wrap

def profile(f):
    async def profiler(*args,**kwargs):
        with cProfile.Profile() as pr:
            result = await f(*args,**kwargs)

        with open('profiling_stats.txt', 'w') as stream:
            stats = Stats(pr, stream=stream)
            stats.strip_dirs()
            stats.sort_stats('time')
            stats.dump_stats('.prof_stats')
            stats.print_stats()
        
        
        return result
    return profiler