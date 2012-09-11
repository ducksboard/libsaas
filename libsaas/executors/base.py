from . import current


def use_executor(executor):
    current.process = executor


def current_executor():
    return current.process
