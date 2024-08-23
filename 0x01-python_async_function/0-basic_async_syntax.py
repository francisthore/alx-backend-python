#!/usr/bin/env python3
""" Module that defines a coroutine that
    waits for a random delay between an
    input 0 and a n input value
"""
import asyncio
import random


async def wait_random(max_delay=10):
    """Waits for a random delay between 0 and the
    passed in value for max_delay
    """
    sleep_time = random.uniform(0, max_delay)
    await asyncio.sleep(sleep_time)
    return sleep_time
