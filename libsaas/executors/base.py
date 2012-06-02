from . import current


def use_executor(executor):
    current.process = executor
