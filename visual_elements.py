"""
  Project Name: Book Scraping Project
  File Name: visual_elements.py

  Description:
    This is the file that contains all of the visual elements such
    as terminal colours and menus.
"""

class MenuBuilder:
    """
    Allows the programmer to quickly
    make a terminal menu using a simple
    builder.
    """

    def add(self, option=""):
        """
        Adds an option to the menu.
        """
        self._items.append(option)

    def get_input(self):
        """
        This gets an input from the user which is
        returned.
        """

        user_question = Fore.BLUE + "\n\n[User Choice]: " + Style.RESET_ALL
        user_input = input(user_question)

        return user_input

    def get_number_input(self, min_num=None, max_num=None):
        """
        This gets a number input with a minimum and maximum,
        this helps to ensure the data is within the range that
        is needed.

        Note:
          if the min or max is None it will remove that aspect
          of the validation from the number, which can be useful
          if you need a number with a minimum and no maximum.
        """
        while True:
            user_input = self.get_input()

            try:
                user_input = int(user_input)
            except ValueError:
                Terminal.print_error(
                    "\nPlease type in a valid numeric option from the menu."
                )
                return None

            if min_num is not None and isinstance(min_num, int):
                if user_input < min_num:
                    Terminal.print_error(
                        "\nPlease type a valid number. (The number is too small.)"
                    )
                    return None

            if max_num is not None and isinstance(max_num, int):
                if user_input > max_num:
                    Terminal.print_error(
                        "\nPlease type a valid number. (The number is too large.)"
                    )
                    return None
            break
        return user_input

    def get_menu_option_input(self):
        """
        This is used to ensure that the input
        provided from the user is valid with the
        current menu that was built.
        """
        while True:
            user_input = self.get_input()

            try:
                user_input = int(user_input)
            except ValueError:
                Terminal.print_error(
                    "\nPlease type in a valid numeric option from the menu."
                )
                return None

            if len(self._items) < user_input > len(self._items):
                Terminal.print_error("\nPlease select an option within the menu range.")
            else:
                break

        return user_input

    def __str__(self):
        """
        Generates the menu into a string
        which allows the user to print it out.
        """
        menu = Fore.RED
        menu += f"\n\n{self._title}\n"
        menu += Style.RESET_ALL
        menu += Fore.GREEN
        ind = 0
        for i in self._items:
            ind += 1
            menu += f"\n[{ind}]: {i}"
        menu += Style.RESET_ALL
        return menu

    def __init__(self, title=""):
        """
        Sets up the menu class.
        """

        self._title = title
        self._items = []
