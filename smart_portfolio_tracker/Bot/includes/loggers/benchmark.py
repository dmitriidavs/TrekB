import logging

from time import perf_counter
from typing import Callable, Any


# TODO: move to online dashboard
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]: %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def benchq(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(f'Query [{func.__name__}] executed in {run_time:.2f} sec')
        return result

    return wrapper
