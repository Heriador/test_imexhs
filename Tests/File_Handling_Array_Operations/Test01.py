import os
import csv
import logging
import pydicom
from datetime import datetime


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def listFolder(path):
    print('List of files in the folder: ' + path)
    try:

        # listing the files in the path folder using os.listdir
        files = os.listdir(path)
        nfiles = 0
        for _ in files:
            
            nfiles += 1

        print('Total files: ' + str(nfiles))

    #Handling the exceptions 
    except FileNotFoundError as e:
        logging.error(f"Folder not found: {e}")
    
    except Exception as e:
        logging.error(f"Error reading folder: {e}")
        
    
   


def read_csv(path,filename):
    
    try:

        #Reading the csv file using the csv library
        file = open(os.path.join(path ,filename), 'r')
        reader = csv.reader(file)

        #Extracting the headers and the data from the csv file
        data = list(reader)
        headers = data[0]

        #Creating a list to store the average and standard deviation of the numeric columns
        average = [0.0 for _ in range(len(data[0]))]
        std = [0.0 for _ in range(len(data[0]))]
       


        #Calculating the average and standard deviation of the numeric columns

        #Iterating through the columns
        for i in range(len(headers)):
            #Verifying if the column is numeric
            if not data[1][i].isnumeric():
                continue

            #Extracting the column and calculating the average and standard deviation
            column = [float(row[i]) for row in data[1:]]
            average[i] = sum(column)/len(column)
            std[i] = (sum([(x-average[i])**2 for x in column])/len(column))**0.5
        

        #Printing the number of columns and the columns in the csv file, as well as the average and standard deviation of the numeric columns
        print(f"Number of columns: {len(headers)} ")
        print(f"Columns: {headers}")
        print("\nColumns: Average, standard deviation")
        for i in range(len(headers)):
            if(average[i] == 0):
                continue
            
            print(f"{headers[i]}: {round(average[i],4)}, {round(std[i],4)}")


    #Handling the exceptions
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return
    
  
   

    
def read_DICOM(path,DICOM_file,tags=[]):
    
    file_path = os.path.join(path,DICOM_file)

    #Checking if the file exists
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return
    
    try:
        #Reading the DICOM file using pydicom
        file_dicom = pydicom.dcmread(file_path)

        #Printing the patient name, study date and modality of the DICOM file
        print(f"Patient Name: {file_dicom.PatientName}")

        #Converting the study date to a readable format
        study_date = datetime.strptime(file_dicom.StudyDate, "%Y%m%d")
        print(f"Study date {study_date.strftime('%d/%m/%Y')}")
        print(f"Modality: {file_dicom.Modality}")

        #Printing the additional tags if they are provided
        print("\nAdditional tags: ")
        if len(tags) > 0:
            for tag in tags:
                element = file_dicom[tag]
                
                print(f'{element.name}: {element.value}')
              

    except Exception as e:
        logging.error(f"Error reading file: {e}")
        

   



if __name__ == '__main__':
    #Path to the parent directory
    base_path = os.path.dirname(__file__)
    sample_directory = os.path.join(base_path, '..', 'samples')

    print("\n\nLIST FOLDER CONTENTS")
    listFolder(sample_directory)

    print("\n\nREAD CSV FILE")
    read_csv(sample_directory, "sample-01-csv.csv")

    print("\n\nREAD DICOM FILE")
    read_DICOM(sample_directory, "sample-01-dicom.dcm",[(0x0008, 0x0005),(0x0008, 0x0016)])