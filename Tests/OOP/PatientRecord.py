import logging
import os
from datetime import datetime

class PatientRecord:
    
    #Constructor of the class with the required attributes
    def __init__(self,name,birth_date,sex,weight,patien_id,type_id) -> None:
        logging.basicConfig(level=logging.DEBUG, 
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filename=f'{os.path.dirname(__file__)}/PatientRecord.log',
                            filemode='a')
        self.__name = name
    
        #Checking if the birth_date is a string or a datetime object and doing the conversion
        if isinstance(birth_date, str):
            self.__birth_date = datetime.strptime(birth_date,"%Y-%m-%d").date()
        elif isinstance(birth_date, int):
            self.__birth_date = datetime(birth_date).date()
        elif isinstance(birth_date, datetime):
            self.__birth_date = birth_date.date()

        #Calculating the age based on the birth_date
        self.calculate_age()

        #Setting the other attributes
        self.__sex = sex
        self.__weight = weight
        self.__patien_id = patien_id
        self.__type_id = type_id

    #Method to update the diagnosis of the patient and log the information
    def update_diagnosis(self,diagnosis):
        logging.info(f"Diagnosis updated: {diagnosis}")


    #Method to calculate the age based on the birth_date
    def calculate_age(self):
        self.set_age(datetime.now().year - self.__birth_date.year)

    #Getters and setters for the attributes
    def get_name(self):
        return self.__name
    
    def set_name(self,name):
        self.__name = name
    
    def get_age(self):
        return self.__age
    
    def set_age(self,age):
        if age < 0:
            raise ValueError("Age cannot be negative")
        self.__age = age

    def get_birth_date(self):
        return self.__birth_date
    
    #Checking if the birth_date is a string or a datetime object and doing the conversion
    def set_birth_date(self,birth_date):
        if isinstance(birth_date, str):
            self.__birth_date = datetime.strptime(birth_date,"%Y%m%d").date()
        elif isinstance(birth_date, datetime):
            self.__birth_date = birth_date.date()
        else:
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD' or a datetime object.")
        
        self.calculate_age()


    def get_sex(self):
        return self.__sex
    
    def set_sex(self, sex):
        self.__sex = sex

    def get_weight(self):
        return self.__weight
    
    def set_weight(self, weight):
        self.__weight = weight

    def get_patient_id(self):
        return self.__patien_id
    
    def set_patient_id(self,patien_id):
        self.__patien_id = patien_id

    def get_type_id(self):
        return self.__type_id
    
    def set_type_id(self,type_id):
        self.__type_id = type_id


    #Method to print the information of the patient
    def __str__(self):
        info = (
            f"Name: {self.__name}\n"
            f"Age: {self.__age}\n"
            f"Birth date: {self.__birth_date}\n"
            f"Sex: {self.__sex}\n"
            f"Weight: {self.__weight}\n"
            f"Patient ID: {self.__patien_id}\n"
            f"Type ID: {self.__type_id}\n"
        )

        return info