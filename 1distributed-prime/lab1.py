from time import time
from math import sqrt, ceil

from multiprocessing import Process, Queue, current_process
from queue import Empty  # exception to break from loop when the get(block=False) called on empty queue


import matplotlib.pyplot as plt


numbers = [15492781, 15492787, 15492803,
           15492811, 15492810, 15492833,
           15492859, 15502547, 15520301, 15527509]



def is_prime(number):
    """returns True if number
    is prime, False otherwise"""
    #for i in range(2, ceil(sqrt(number))):
    for i in range(2, number):
        if number % i == 0:
            return False
    return True



def check_prime_worker(job_queue):
    """worker function passed as target to Process"""
    while True:
        # your code here
        # 1. get next available number from queue
        try:
            number = job_queue.get(block=False)
            print(f"Process {current_process()} checks number {number}")
        except Empty:
            break

        # 2. print the number and whether it
        #    is prime or not, use is_prime()
        if is_prime(number):
            print(f"{number} is prime")
        else:
            print(f"{number} is not prime")

        # 3. use try/except to catch Empty exception
        #    and quit the loop if no number remains in queue
        #    done in step 1


if __name__ == "__main__":
    start = time()

    for number in numbers:
        if is_prime(number):
            print(f"{number} is prime")
        else:
            print(f"{number} is not prime")

    t_seq = time()
    print(f"Performance: {t_seq - start}")


    job_queue = Queue()
    t_par = []

    # number of workers
    for N in range(1, len(numbers) + 1):
        # preparing the jobs to be done by workers
        for number in numbers:
            job_queue.put(number)

        # your code here

        # 1. create list of processes of N process. Choose N in range of [1:len(numbers)]
        processes = [Process(target=check_prime_worker, args=(job_queue,)) for i in range(N)]

        # 2. record the start time
        start = time()

        # 3. start each of the processes
        [p.start() for p in processes]

        # 4. call join on each of the processes
        [p.join() for p in processes]

        # 5. measure the performance and append to the list of records
        t_par.append(time() - start)

        # 6. close the processes
        [p.close() for p in processes]



    fig, ax = plt.subplots()
    y = list(map(lambda x: t_seq / x, t_par))
    ax.plot(range(1, len(numbers) + 1), y)

    ax.set(xlabel='number of processes', ylabel='time(s)',
           title='Dependence of performance on number of processes')

    plt.show()
