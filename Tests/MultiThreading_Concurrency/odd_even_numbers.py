import threading
import time

#Using lock prevents the threads from printing at the same time 
print_lock = threading.Lock()


#Function to print odd and even numbers
def print_odd():
    print("Odd numbers:")
    for i in range(1,201):
        if i % 2 != 0:
            #the even numbers are printed after a delay of 0.5 seconds
            time.sleep(0.5)
            #Using the lock to prevent the threads from printing at the same time
            with print_lock:
              print("Odd number: ",i)


#Function to print even numbers
def print_even():
    print("Even numbers:")
    for i in range(1,201):
        if i % 2 == 0:
            #the even numbers are printed after a delay of 0.5 seconds
            time.sleep(0.5)
            #Using the lock to prevent the threads from printing at the same time
            with print_lock:
              print("even number:",i)





if __name__ == "__main__":
    
    #Starting the timer
    t = time.time()

    #Creating the threads
    t1 = threading.Thread(target=print_odd)
    t2 = threading.Thread(target=print_even)

    #Starting the threads
    t1.start()
    t2.start()

    #Joining the threads so that the main thread waits for the threads to finish
    t1.join()
    t2.join()

    #Printing the time taken
    print("Time taken:", time.time()-t)

