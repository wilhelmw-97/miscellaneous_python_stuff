import time, threading



def print_a():
    global a, lock
    for i in range(0, 16):
        lock.acquire()
        print 'p_a: ', a
        time.sleep(1)

def print_b():
    global b, lock
    for i in range(0, 16):
        lock.acquire()
        print 'p_b: ', b
        time.sleep(1)

a = 'a1'
b = 'b1'
ta = threading.Thread(target= print_a)
tb = threading.Thread(target= print_b)
ta.start()
tb.start()
lock = threading.Lock()
time.sleep(3)
a = 'a2'
time.sleep(1)
b = 'b2'
time.sleep(4)
a = 'a3'