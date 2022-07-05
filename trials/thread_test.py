import _thread
import time

def first_thread():
    print("First thread")
    time.sleep(1)


_thread.start_new_thread(first_thread, ())

print(first_thread.__name__)