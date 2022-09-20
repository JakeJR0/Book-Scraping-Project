import re as regex
import pandas as pd
import sqlite3, os

colours = None

class ExportError(SystemError):
  """
    Used to inform the user that the export failed.
  """

class FileController:
  @property
  def cursor(self):
    """
      Creates a cursor object and returns it.
    """
    return self._con.cursor()

  def save(self):
    """
      Saves changes to the database
    """

    self._con.commit()

  def _valid_book_title(self, title=""):
    """
      Checks that the title is not already within
      the database.
    """
    
    valid_title = True
    cur = self.cursor
    titles = cur.execute('''
      SELECT
        LOWER(book_title) AS title
      FROM
        books
    ''')
    
    title = title.lower()
    for i in titles:
      if i[0] == title:
        valid_title = False
        break
        
    cur.close()    
    
    return valid_title

  def export(self, file_name=""):
    # CSV Seleted
    cur = self.cursor

    if os.path.exists(file_name):
      raise ExportError("File already exists, please try a different name.")
      return
    
    if regex.match("(\S+)\.csv", file_name):
      colours.print_message("\nExporting to CSV (This might take a while)\n")
      export = cur.execute('''
        SELECT
          ID,
          book_title,
          book_description,
          book_cover,
          book_link
        FROM
          books
      ''')

      frame = pd.DataFrame({
        "ID": [],
        "book_title": [],
        "book_description": [],
        "book_cover": [],
        "book_link": []
      })

      for i in export:
        frame.loc[len(frame.index)] = list(i)

      frame.to_csv(file_name,index=False)
      
    elif regex.match("(\S+)\.json", file_name):
      colours.print_message("\nExporting to JSON (This might take a while)\n")
      export = cur.execute('''
        SELECT
          ID,
          book_title,
          book_description,
          book_cover,
          book_link
        FROM
          books
      ''')

      frame = pd.DataFrame({
        "ID": [],
        "book_title": [],
        "book_description": [],
        "book_cover": [],
        "book_link": []
      })

      for i in export:
        frame.loc[len(frame.index)] = list(i)

      frame.to_json(file_name)
        
    elif regex.match("(\S+)\.sql", file_name):
      colours.print_message("\nExporting to SQL (This might take a while)\n")
      sql_insert = "INSERT INTO books(ID, book_title, book_description, book_cover, book_link)"
      sql_insert += "\nVALUES"

      export = cur.execute('''
        SELECT
          ID,
          book_title,
          book_description,
          book_cover,
          book_link
        FROM
          books
      ''')

      for i in export:
        line = "\n('{}', '{}','{}','{}','{}')"
        line = line.format(i[0], i[1], i[2], i[3], i[4])
        sql_insert += line

      with open(file_name, "x") as f:
        f.write(sql_insert)

    else:
      error_message = "The extension provided is not supported.\n"
      error_message += "(Currently Supporting: CSV, JSON, SQL)"
      cur.close()
      raise ExportError(error_message)

    colours.print_message("Exported successfully to {}".format(file_name))
    cur.close()
      
  
  def view_latest_book_titles_frame(self, limit=None):
    cur = self.cursor
    data = None
    if limit is None:
      data = cur.execute('''
        SELECT
          ID,
          book_title
        FROM
          books
        ORDER BY
          ID DESC
      ''')
    else:
      if type(limit) != int:
        raise ValueError("Limit provided is not an integer.")
        return

      if limit <= 0:
        raise ValueError("Limit provided must be higher than 0.")
        return

      data = cur.execute('''
        SELECT
          ID,
          book_title
        FROM
          books
        ORDER BY
          ID DESC
        LIMIT
          ?
      ''', (limit, ))

    frame = pd.DataFrame({
      "book_id": [],
      "book_title": []
    })

    for i in data:
      frame.loc[len(frame.index)] = [i[0], i[1]]
      
    cur.close()
    return frame

      
      

  def add(self, title="", desc="", thumb="", link=""):
    """
      Adds a row to the books table
    """

    # Ensures the description has a string value
    
    if desc == "None" or desc is None:
      desc = "Not Found"
    
    # Cleans the data from containing "'"

    title = title.replace("'", "")
    desc = desc.replace("'", "")
    thumb = thumb.replace("'", "")
    link = link.replace("'", '')

    # Ensures the title does not exist

    if not self._valid_book_title(title):
      book_exists_warning = "{} already exists in the database. (Skipped)".format(title)

      try:
        colours.print_warning(book_exists_warning)
      except AttributeError:
        print(book_exists_warning + " (FileControl was not setup)")
      return 
      
    # Creates the cursor object

    cur = self.cursor
    
    # Inserts the book into the database.
      
    cur.execute('''
      INSERT INTO books(book_title, book_description, book_cover, book_link)
      VALUES
      (?, ?, ?, ?)
    ''', (title, desc, thumb, link))

    cur.close()

    # Saves the change to the database
    
    self.save()

  def __str__(self):
    """
      Displays the amount of books registered
      when the class is printed.
    """
    cur = self.cursor
    cur.execute('''
      SELECT
        COUNT(*)
      FROM
        books
    ''')
    book_count = cur.fetchone()[0]
    cur.close()
    
    output = "Currently we have {} books registered within the database.".format(book_count)
    
    return output
      
      
  def __init__(self, file_name="storage.db"):
    """
      Sets up the file controller class to ensure it can
      function as intended.
    """
    file_name_valid = regex.match("(\S+)\.db", file_name)

    if not file_name_valid:
      raise ValueError("File name not meeting the requirements.")
    
    self._file = file_name
    
    self._con = sqlite3.connect(self._file)

    cur = self.cursor
    
    cur.execute('''
      CREATE TABLE IF NOT EXISTS books(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        book_title TEXT NOT NULL,
        book_description TEXT NOT NULL,
        book_cover TEXT NOT NULL,
        book_link TEXT NOT NULL
      )
    ''')

    cur.close()

def setup(**kwargs):
  global colours
  
  terminal_colors = kwargs["terminal_colors"]
  colours = terminal_colors
    
if __name__ == "__main__":
  FileController()