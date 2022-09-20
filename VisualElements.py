from colorama import Fore, Style


class Terminal:
    """
    This is used to orgainise the functions
    so it is easier to import into other files.
    """

    @classmethod
    def print_error(self, text=""):
        """
        This is the standard colouring for an
        error message in this program.
        """
        output = Fore.RED + text + Style.RESET_ALL
        print(output)

    @classmethod
    def print_warning(self, text=""):
        """
        This is the standard colouring for a
        warning message in this program.
        """
        output = Fore.YELLOW + text + Style.RESET_ALL
        print(output)

    @classmethod
    def print_message(self, text=""):
        """
        This is the standard colouring for a
        message in this program.
        """
        output = Fore.GREEN + text + Style.RESET_ALL
        print(output)


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

    def get_number_input(self, min=None, max=None):
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
            except BaseException:
                Terminal.print_error(
                    "\nPlease type in a valid numeric option from the menu."
                )
                return

            if min is not None and type(min) == int:
                if user_input < min:
                    Terminal.print_error(
                        "\nPlease type a valid number. (The number is too small.)"
                    )
                    return

            if max is not None and type(max) == int:
                if user_input > max:
                    Terminal.print_error(
                        "\nPlease type a valid number. (The number is too large.)"
                    )
                    return
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
            except BaseException:
                Terminal.print_error(
                    "\nPlease type in a valid numeric option from the menu."
                )
                return

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
        menu += "\n\n{}\n".format(self._title)
        menu += Style.RESET_ALL
        menu += Fore.GREEN
        ind = 0
        for i in self._items:
            ind += 1
            menu += "\n[{}]: {}".format(ind, i)
        menu += Style.RESET_ALL
        return menu

    def __del__(self):
        """
        Allows the class to be deleted.
        """

        pass

    def __init__(self, title=""):
        """
        Sets up the menu class.
        """

        self._title = title
        self._items = []
