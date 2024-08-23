#!/usr/bin/env python3
"""Module that defines a routine that imports the
wait_random coroutine and spawns it n times"""
import asyncio
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


def return_sorted_list(unsorted_list: List[float]) -> List[float]:
    """Returns a sorted list"""
    return sorted(unsorted_list)


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """Spawns a corouting up to n times with max_delay
    as the input and returns the list of delays"""
    input = []
    for i in range(n):
        input.append(task_wait_random(max_delay))
    res = await asyncio.gather(*input)
    return return_sorted_list(res)
