from colorama import Fore, Style

class Terminal:
  @classmethod
  def print_error(self, text=""):
    output = Fore.RED + text + Style.RESET_ALL
    print(output)
  
  @classmethod
  def print_warning(self, text=""):
    output = Fore.YELLOW + text + Style.RESET_ALL
    print(output)
    
  @classmethod
  def print_message(self, text=""):
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
    user_question = Fore.BLUE + "\n\n[User Choice]: " + Style.RESET_ALL
    user_input = input(user_question)
    
    return user_input

  def get_number_input(self, min=None, max=None):
    while True:
      user_input = self.get_input()
      
      try:
        user_input = int(user_input)
      except BaseException:
        Terminal.print_error("\nPlease type in a valid numeric option from the menu.")
        return

      if min is not None and type(min) == int:
        if user_input < min:
          Terminal.print_error("\nPlease type a valid number. (The number is too small.)")
          return

      if max is not None and type(max) == int:
        if user_input > max:
          Terminal.print_error("\nPlease type a valid number. (The number is too large.)")
          return
      break
    return user_input
      
        
        
  
  def get_menu_option_input(self):
    while True:
      user_input = self.get_input()
      
      try:
        user_input = int(user_input)
      except BaseException:
        Terminal.print_error("\nPlease type in a valid numeric option from the menu.")
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
    