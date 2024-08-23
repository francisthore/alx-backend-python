#!/usr/bin/env python3
"""Module that defines a routine that calculates
program execution duration"""
import asyncio
import time
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """Measures the execution time of a routine"""
    start: float = time.time()
    asyncio.run(wait_n(n, max_delay))
    end: float = time.time()

    res = (end - start) / n

    return res
