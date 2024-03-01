from collections import defaultdict
from typing import Callable
import sys

ANIM_BREAKPOINT_HOOK = None

def set_anim_breakpoint_hook(hook: Callable):
    global ANIM_BREAKPOINT_HOOK
    ANIM_BREAKPOINT_HOOK = hook

def abreakpoint(state, *args, **kwargs):
    if ANIM_BREAKPOINT_HOOK is not None:
        ANIM_BREAKPOINT_HOOK(state, sys._getframe(1), args, kwargs)

def invert_dict(dico: dict) -> dict:
    res = defaultdict(list)

    for k, v in dico.items():
        res[v].append(k)

    return dict(res)
