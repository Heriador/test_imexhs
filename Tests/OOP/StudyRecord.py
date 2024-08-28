import pydicom
from PatientRecord import PatientRecord
from datetime import datetime, time

# Class to store the information of a study record of a patient
class StudyRecord(PatientRecord):

  def __init__(self):
     super().__init__()


  #Constructor of the class with the required attributes
  def __init__(self, name,birth_date,sex,weight,patien_id,type_id,study_date,modality,study_time,study_instance_uid,series_number,number_frames):
    super().__init__(name,birth_date,sex,weight,patien_id,type_id)
    self.__study_date = study_date
    self.__modality = modality
    self.__study_time = study_time
    self.__study_instance_uid = study_instance_uid
    self.__series_number = series_number
    self.__number_frames = number_frames


  #Getters and setters for the attributes
  def get_study_date(self):
    return self.__study_date
  
  #Checking if the study_date is a string or a datetime object and doing the conversion
  def set_study_date(self,study_date):
    if isinstance(study_date, str):
        self.__study_date = datetime.strptime(study_date, "%Y%m%d").date()
    elif isinstance(study_date, datetime):
        self.__study_date = study_date.date()
    

  def get_modality(self):
    return self.__modality
  
  def set_modality(self,modality):
    self.__modality = modality

  def get_study_time(self):
    return self.__study_time

  #Checking if the study_time is a string or a datetime object and doing the conversion
  def set_study_time(self,study_time):
      if isinstance(study_time, str):
            self.__study_time = datetime.strptime(study_time,"%H%M%S").time()
      elif isinstance(study_time, datetime):
            self.__study_time = study_time.time()
      elif isinstance(study_time, datetime.time):
            self.__study_time = study_time

  def get_study_instance_uid(self):
    return self.__study_instance_uid
  
  def set_study_instance_uid(self,study_instance_uid):
    self.__study_instance_uid = study_instance_uid

  def get_series_number(self):
    return self.__series_number
  
  def set_series_number(self,series_number):
    self.__series_number = series_number

  def get_number_frames(self):
    return self.__number_frames
  
  def set_number_frames(self,number_frames):
    self.__number_frames = number_frames

  #Method to load the information from a DICOM file
  def load_from_dicom(self, dicom_file_path):
        dicom_data = pydicom.dcmread(dicom_file_path)    
        # print(dir(dicom_data))

        #Setting the attributes of the patient record if they are present in the DICOM file
        self.set_name(dicom_data.PatientName if 'PatientName' in dicom_data else self.get_name())
        self.set_birth_date(dicom_data.PatientBirthDate if 'PatientBirthDate' in dicom_data else self.get_birth_date())
        self.set_sex(dicom_data.PatientSex if 'PatientSex' in dicom_data else self.get_sex())
        self.set_patient_id(dicom_data.PatientID if 'PatientID' in dicom_data else self.get_patient_id())        

        #Setting the attributes of the study record
        self.set_study_date(dicom_data.StudyDate if 'StudyDate' in dicom_data else None)
        self.set_modality(dicom_data.Modality if 'Modality' in dicom_data else None)
        self.set_study_time(dicom_data.StudyTime if 'StudyTime' in dicom_data else None)
        self.set_study_instance_uid(dicom_data.StudyInstanceUID if 'StudyInstanceUID' in dicom_data else None)
        self.set_series_number(dicom_data.SeriesNumber if 'SeriesNumber' in dicom_data else None)
        self.set_number_frames(dicom_data.NumberOfFrames if 'NumberOfFrames' in dicom_data else None)
        
  #Method to print the information of the study record
  def __str__(self):
        patient_info = super().__str__()
        study_info = (
            f"Study Date: {self.__study_date}\n"
            f"Modality: {self.__modality}\n"
            f"Study Time: {self.__study_time}\n"
            f"Study Instance UID: {self.__study_instance_uid}\n"
            f"Series Number: {self.__series_number}\n"
            f"Number of Frames: {self.__number_frames}\n"
        )
        return f"{patient_info}\n{study_info}"