"""
Basic module for using purpose of provining temporary memory
for sharing data by different modules.
"""

from core.utils.manager import StateCache

config = {}
cache = StateCache()
config["cache"] = cache
