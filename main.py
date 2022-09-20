from GoodReads import GoodReads
from GoodReads import setup as goodreads_setup
from GoodReads import file
from GoodReads import FileControl
from VisualElements import Terminal as colours
from VisualElements import MenuBuilder
from time import sleep


def main_menu():
  main_menu_object = MenuBuilder("Welcome to the Book Scraper")
  main_menu_object.add("Scrape the Web")
  main_menu_object.add("View")
  main_menu_object.add("Export")
  main_menu_object.add("Exit Program")
  
  while True:
    try:
      print(main_menu_object)
      choice = main_menu_object.get_menu_option_input()
  
      # User selected Scrape Web
      if choice == 1:
        sites_options = MenuBuilder("Website Options")
        sites_options.add("GoodReads")
  
        while True:
          try:
            print(sites_options)
            selected_site = sites_options.get_menu_option_input()
            
            # User Selected GoodReads as the site
            
            if selected_site == 1:
              try:
                print("\n\n")
                GoodReads()
              except KeyboardInterrupt:
                break
            
          except KeyboardInterrupt:
            break
            
      elif choice == 2:
        view_menu = MenuBuilder("View Menu")
        view_menu.add("View last 50 Books")
        view_menu.add("View Custom Amount of Books")
        view_menu.add("View All Books")
        view_menu.add("Exit Menu")

        while True:
          try:
            print(view_menu)
            user_choice = view_menu.get_menu_option_input()

            if user_choice == 1:
              frame = file.view_latest_book_titles_frame(50)
              print(frame.to_string())
              sleep(2)
            elif user_choice == 2:
              colours.print_message("\n\nPlease specify the amount of books to view")
              books_to_view = view_menu.get_number_input(1)
              frame = file.view_latest_book_titles_frame(books_to_view)
              print(frame.to_string())
              sleep(2)
              
            elif user_choice == 3:
              frame = file.view_latest_book_titles_frame()
              print(frame.to_string())
              sleep(4)
            elif user_choice == 4:
              break
              
          except KeyboardInterrupt:
            break
      elif choice == 3:
        while True:
          try:
            colours.print_message("\n\nPlease type in the file name including the file extension.")
            export_name = main_menu_object.get_input()
            file.export(export_name)
            break
          except KeyboardInterrupt:
            break
          except FileControl.ExportError as e:
            colours.print_error("\n\nFailed to export with reason: {}".format(e))
        sleep(4)
            
      elif choice == 4:
        colours.print_message("\n\nThank you for using the Book Scraper.")
        break
        
    except KeyboardInterrupt:
      colours.print_message("\n\nThank you for using the Book Scraper.\n\n")
      break
      
      
  

  
if __name__ == "__main__":
  goodreads_setup(terminal_colors=colours)
  main_menu()