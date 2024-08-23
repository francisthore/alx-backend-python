#!/usr/bin/env python3
"""Module that defines a routine that imports the
wait_random coroutine and spawns it n times"""
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> float:
    """Spawns a corouting up to n times with max_delay
    as the input and returns the list of delays"""
    input = []
    for i in range(n):
        input.append(wait_random(max_delay))
    res = await asyncio.gather(*input)
    return (sorted(res))
