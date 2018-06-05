import multiprocessing
from multiprocessing import Process,Queue
import time
import sys
import random

"""

A simple program that illustrates Multiprocessing in Python.
This is a program to generate N random integers and calculate their sum. I spawn 4 threads in parallel. Each thread computes the sum of N/4 integers and the results are then merged.

"""

def generateRandomNumbers(n):
    list = []
    for i in range(int(n)):
        value = random.randint(0,10)
        list.append(value)
    print("Random generated numbers are" + str(list))
    return list

def computeSum(list):
    sum = 0
    for number in list:
        sum += number
    return sum


def compute(size,queue):
    list = generateRandomNumbers(size)   #of size n/4
    sum = computeSum(list)
    queue.put(sum)  #put results in the queue



if __name__ == '__main__':
    size = 20 #number of integers
    start = time.time()
    queue = Queue()
    thread1 = Process(target=compute, args=(size/4,queue))
    thread1.start()
    thread2 = Process(target=compute, args=(size/4,queue))
    thread2.start()
    thread3 = Process(target=compute, args=(size/4,queue))
    thread3.start()
    thread4 = Process(target=compute, args=(size/4,queue))
    thread4.start()

    #get results from the queue

    results = []
    for i in range(4):
        #print("Partial sum for thread" + str(i+1) + "is "+ str(queue.get(True)))
        results.append(queue.get(True))

    print("These are the partial results")
    for i,partial_sum in enumerate(results):
        print("Partial sum for thread " + str(i+1) + " is "+ str(partial_sum))

    #sum these partial results to get the final result

    print("\n\n------Merging the results------")
    final_sum = computeSum(results)

    # join() will wait until all child threads complete its execution and then only main method will exit.
    thread1.join()  #wait for the thread to complete its work
    thread2.join()
    thread3.join()
    thread4.join()

    end = time.time()
    print("Total time to execute the task!"+ str(end-start))
    print("final sum is " + str(final_sum))