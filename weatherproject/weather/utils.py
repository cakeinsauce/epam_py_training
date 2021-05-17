from datetime import datetime
from typing import Dict


def temp_param_validate(params: Dict[str, str]) -> str:
    """Validate query temperature parameter."""
    temp = params.get("u")
    if temp not in ("celsius", "fahrenheit"):
        return "celsius"
    return temp


def period_params_validate(params: Dict[str, str]):
    """Validate query period parameters"""
    start_lb = ("s", "0001-01-01_00-00")
    finish_lb = ("f", "9999-12-31_23-59")

    start_finish = []

    for label in start_lb, finish_lb:
        dt = params.get(label[0])
        try:
            dt = datetime.strptime(dt, "%Y-%m-%d_%H-%M")
        except (TypeError, ValueError):
            dt = datetime.strptime(label[1], "%Y-%m-%d_%H-%M")
        finally:
            start_finish.append(dt)

    return start_finish
