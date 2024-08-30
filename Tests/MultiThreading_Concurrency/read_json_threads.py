import logging.handlers
import threading
import os
import json
from concurrent.futures import ThreadPoolExecutor
import logging
from queue import Queue

#Creating a queue to store the logs
log_queue = Queue()

#Creating a queue handler
queue_handler = logging.handlers.QueueHandler(log_queue)

#Creating a file handler
file_handler = logging.FileHandler(f'{os.path.dirname(__file__)}/json_results.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

#Creating a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(queue_handler)

#Creating a queue listener
queue_listener = logging.handlers.QueueListener(log_queue, file_handler)
queue_listener.start()

#Using lock prevents the threads from printing at the same time
print_lock = threading.Lock()


#Function to process the element in the json file
def process_element(element):

    #Extracting the element id and data from the element
    element_id = element['id']
    element_data = element['data']

    #Transforming the data in the element to an array of integers
    element_data = [[int(num) for num in line.split() ] for line in element_data]
    element_data = [num for line in element_data for num in line]

    #Normalizing the data in the element
    element_max_value = max(element_data)
    element_data_normalized = [round(num / element_max_value, 4) for num in element_data]
    
    #Calculating the average of the data before and after normalization
    element_data_average = sum(element_data) / len(element_data)
    element_data_normalized_average = sum(element_data_normalized) / len(element_data_normalized)

   
    #Logging and printing the results
    with print_lock:

        logger.info(f"Element ID: {element_id}")
        logger.info(f"data average before normalization: {element_data_average}")
        logger.info(f"data average after normalization: {element_data_normalized_average}")
        logger.info(f"data size : {len(element_data)}")
        logger.info("*************************************************"*len(element_data))

        print(f"Element ID: {element_id}")
        print(f"data average before normalization: {element_data_average}")
        print(f"data average after normalization: {element_data_normalized_average}")
        print(f"data size : {len(element_data)}")
        print("\n")

#Function to read the json file and return the data
def read_json(json_file_path):
    print("Reading the json file")
    file = open(json_file_path)
    data = json.load(file)
     
    print("Json file read successfully\n")

    return data


#Function to create the threads for the elements in the json file
def create_threads(data):

    #Creating the thread pool with max of 4 threads
    with ThreadPoolExecutor(max_workers=4) as executor:

        #Submitting the tasks to the thread pool for each element in the json file
        results = [executor.submit(process_element, element) for element in data.values()]

        #Printing the results
        for result in results:
            result.result()





if __name__ == "__main__":
  
  #Setting the base path
  base_path = os.path.dirname(__file__)

  #Setting the path to the json file
  sample_directory = os.path.join(base_path, '..', 'samples')
  json_file_path = os.path.join(sample_directory, "sample-03-01-json.json")

  #Reading the json file
  data = read_json(json_file_path)

  #Creating the threads for the elements in the json file
  create_threads(data)
