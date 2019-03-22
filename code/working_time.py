import time

def working_time(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        c = function(*args, **kwargs)
        end_time = time.time()
        with open('working_time.txt', 'a') as fout:
            fout.write('\nfunction {} worked at {:.2f} seconds'.format(function.__name__, end_time - start_time, 3))
        return c
    return wrapper
