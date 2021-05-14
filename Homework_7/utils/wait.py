import time

import exceptions


def wait(method, error=Exception, timeout=10, interval=0.5, **kwargs):
    st = time.perf_counter()
    last_exception = None
    while time.perf_counter() - st < timeout:
        try:
            result = method(**kwargs)
            return result
        except error as e:
            last_exception = e
        time.sleep(interval)

    raise exceptions.WaitTimeoutException(
        f'Function {method.__name__} timeout in {timeout}sec with exception: "{last_exception}"')
