#1

import queue
import threading

q1 = queue.Queue()
q2 = queue.Queue()
q3 = queue.Queue()


def worker1(thread_id, q):
    while True:
        message = q.get()
        if message is None:
            break
        print(f"Thread {thread_id}: {message['t']}")


def main():

    queue_map = {1: q1, 2: q2, 3: q3}

    threads = []


    for i in range(1, 4):
        t = threading.Thread(target=worker1, args=(i, queue_map[i]))
        t.start()
        threads.append(t)


    while True:
        try:
            t_num = int(input("Enter thread number (1, 2, 3) or 0 to exit: "))
            if t_num == 0:
                break
            if t_num not in queue_map:
                print("Wrong number.")
                continue
            msg = input("Enter your message: ")

            msg_dict = {'n': t_num, 't': msg}
            queue_map[t_num].put(msg_dict)
        except ValueError:
            print("Wrong choice.")


    for q in queue_map.values():
        q.put(None)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()

#2

import threading
import queue
import random
import time


task_queue = queue.Queue()

def worker2(thread_id, q):
    while True:
        number = q.get()
        if number is None:
            break
        print(f"Worker {thread_id} received number {number}")
        time.sleep(number)
        print(f"Worker {thread_id} finished for {number} seconds")

def main2():
    threads = []


    for i in range(1, 4):
        t = threading.Thread(target=worker2, args=(i, task_queue))
        t.start()
        threads.append(t)

    for _ in range(10):
        time.sleep(5)
        number = random.randint(1, 10)
        print(f"Generated Number {number}")
        task_queue.put(number)

    for _ in range(3):
        task_queue.put(None)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main2()