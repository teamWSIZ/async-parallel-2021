import asyncio
import threading


def task_name():
    return asyncio.current_task().get_name()


def thread_name():
    return threading.current_thread().name