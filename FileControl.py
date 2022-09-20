import os
import re as regex
import pandas as pd
from datetime import datetime

class FileController:

  def add(self, title="", desc="", thumb="", link=""):
    title = title.replace("'", "")
    desc = desc.replace("'", "")
    thumb = thumb.replace("'", "")
    link = link.replace("'", '')
    with open(self._file, "a") as f:
      line = "\n{}, {}, {}, {}".format(title, desc, thumb, link)

      f.write(line)
  
  def __del__(self):
    if self._convert:
      frame = pd.read_csv(self._file)
      with open(self.file[:-4] + ".sql", "x") as f:
        
        f.write("INSERT INTO products(title, description, thumbnail, link) VALUES\n")
        
        for i in frame.index:
          title = frame.loc[i, "title"]
          desc = frame.loc[i, "description"]
          thumb = frame.loc[i, "thumbnail"]
          link = frame.loc[i, "link"]
  
          sql_line = "('{}', '{}', '{}', '{}')\n".format(title, desc, thumb, link)
          f.write(sql_line)
          

      
      if self._remove_on_convert:
        os.remove(self._file)

      
  def __init__(self, file_name="file.csv", stamp=True, convert_to_sql=True, remove_on_convert=False):
    file_name_valid = regex.match("(\S+)\.csv", file_name)

    if not file_name_valid:
      raise ValueError("File name not meeting the requirements.")

    self._convert = convert_to_sql
    self._remove_on_convert = remove_on_convert
    
    current_date = datetime.now().strftime("%H-%M_%d-%m-%Y")
    file_template = "{}_{}".format(current_date, file_name)

    self._file = file_template

    with open(self._file, "x") as f:
      f.write("title, description, thumbnail, link")

    
if __name__ == "__main__":
  FileController()