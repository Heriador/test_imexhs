from StudyRecord import StudyRecord
from PatientRecord import PatientRecord
import os

def main():

  base_path = os.path.dirname(__file__)
  sample_directory = os.path.join(base_path, '..', 'samples')

  study_record = StudyRecord("John Doe", "1995-01-01", "M", 75, "1234", "ID", "2021-01-01", "CT", "12:00:00", "1234", "1",3)
  study_record.load_from_dicom(os.path.join(sample_directory, "sample-02-dicom.dcm"))
  study_record.update_diagnosis("Normal")
  print(study_record)

if __name__ == '__main__':
  main()