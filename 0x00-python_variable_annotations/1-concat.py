#!/usr/bin/env python3
"""
    Module that defines a function which is typed
    that concatenates two strings
"""


def concat(str1: str, str2: str) -> str:
    """
        Concatenates two strings
    """
    return '{}{}'.format(str1, str2)
