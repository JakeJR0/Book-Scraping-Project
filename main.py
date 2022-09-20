"""
  Project Name: Book Scraping Project
  File Name: main.py

  Description:
    This is the main file for the Book Scraping Project.
"""

from time import sleep
from colorama import Fore, Style
from good_reads import good_reads
from good_reads import file
from good_reads import file_control
from visual_elements import MenuBuilder

class Terminal:
    """
    This is used to orgainise the functions
    so it is easier to import into other files.
    """

    @classmethod
    def print_error(cls, text=""):
        """
        This is the standard colouring for an
        error message in this program.
        """
        output = Fore.RED + text + Style.RESET_ALL
        print(output)

    @classmethod
    def print_warning(cls, text=""):
        """
        This is the standard colouring for a
        warning message in this program.
        """
        output = Fore.YELLOW + text + Style.RESET_ALL
        print(output)

    @classmethod
    def print_message(cls, text=""):
        """
        This is the standard colouring for a
        message in this program.
        """
        output = Fore.GREEN + text + Style.RESET_ALL
        print(output)


def sites_menu():
    """
    This is a sub-menu that allows the user to select
    which site they want to scrape.
    """
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
                    good_reads()
                except KeyboardInterrupt:
                    break

        except KeyboardInterrupt:
            break


def view_data_menu():
    """
      This allows the user to view the data that has been scraped.
    """

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
                Terminal.print_message("\n\nPlease specify the amount of books to view")
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


def main_menu():
    """
    This allows the user to navigate the program.
    """
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
                sites_menu()

            elif choice == 2:
                view_data_menu()
            elif choice == 3:
                while True:
                    try:
                        Terminal.print_message(
                            "\n\nPlease type in the file name including the file extension."
                        )
                        export_name = main_menu_object.get_input()
                        file.export(export_name)
                        break
                    except KeyboardInterrupt:
                        break
                    except file_control.ExportError as error:
                        error_message = f"\n\nFailed to export with reason: {error}"
                        Terminal.print_error(error_message)
                sleep(4)

            elif choice == 4:
                Terminal.print_message("\n\nThank you for using the Book Scraper.")
                break

        except KeyboardInterrupt:
            Terminal.print_message("\n\nThank you for using the Book Scraper.\n\n")
            break


if __name__ == "__main__":
    main_menu()
