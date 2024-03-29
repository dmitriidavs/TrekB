from functools import wraps
from time import perf_counter
from typing import Callable, Any, Optional

from . import logger


def bench_query(func: Callable[..., Any]) -> Callable[..., Any]:
    """Logs query performance"""
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        logger.info(f'Query [{func.__name__}] executed in {run_time:.6f} sec')
        return result
    return wrapper


def log_ux(btn: str, state: Optional[str] = None, clbck: Optional[str] = None) -> Callable[..., Any]:
    """Logs user actions"""
    
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            logger.info(f'User @{args[0]["from"]["username"]} clicked \'{btn}\'' +
                        (f' -> State: \'{state}\'' if state is not None else '') +
                        (f' -> Callback: \'{clbck}\'' if clbck is not None else ''))
            return result
        return wrapper
    return decorator
