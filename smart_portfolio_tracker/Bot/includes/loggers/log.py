"""
TrekB | Smart Portfolio Tracker
:copyright: (c) 2023 by Dmitrii Davletshin (@dmitriidavs)
:license: BSD-3-Clause, see LICENSE for more details
"""

from functools import wraps

from time import perf_counter
from typing import Callable, Any, Optional

from includes.loggers.log_config import basic_log


def bench_query(func: Callable[..., Any]) -> Callable[..., Any]:
    """Logs query performance"""
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        basic_log.info(f'Query *{func.__name__}* executed in {run_time:.2f} sec')
        return result
    return wrapper


def log_ux(btn: str, state: Optional[str] = None) -> Callable[..., Any]:
    """Logs user actions"""
    
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            basic_log.info(f'User @{args[0]["from"]["username"]} clicked \'{btn}\'' +
                           (f' -> \'{state}\'' if state is not None else ''))
            return result
        return wrapper
    return decorator
