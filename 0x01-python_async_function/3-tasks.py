#!/usr/bin/env python3
"""Module that defines a function that
imports a coroutine and sets it to a task
then return the task"""
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """Creates a task using asyncio"""
    task = asyncio.create_task(wait_random(max_delay))

    return(task)
