import functools


def commonlib_collect(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('call %s():' % func.__name__)
        if len(args) > 0:
            print('args = {}'.format(*args))
        result = func(*args, **kwargs)
        print("func result " + str(result))
        return result

    return wrapper
