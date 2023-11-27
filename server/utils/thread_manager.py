import threading

def on_thread(func):

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=(func), args=args, kwargs=kwargs)
        thread.start()

    return wrapper