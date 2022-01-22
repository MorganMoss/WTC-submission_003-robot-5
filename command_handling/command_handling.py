from .input_exceptions import InputError


class CommandHandler():
    """
    Handles the process of getting user input
    and processing it into commands
    """


    def __init__(self, command_dict:dict) -> None:
        """        
        Constructor for CommandHandling. 
        Assigns a given dictionary to itself.

        Args:
            command_dict (dict): The command dict from the
            instance of ToyRobot this was created by
        """
        self.command_dict = command_dict


    def command_word_valid(self, command:list) -> None:
        """
        Checks if the command word at the beginning
        of the given input exists in the command dictionary

        Args:
            command (list): The user's input, split.

        Raises:
            InputError: If the command does not exist.
        """
        if  command[0].upper() not in self.command_dict:
            raise InputError(command)


    def convert_command_args(self, arg_type:type, command_iter:iter):

        """
        Tries to convert the next or all the following
        command words into their the required type.

        Args:
            arg_type (type): The type the command needs to be converted to.
            command_iter (iter): Iterable containing the command, word by word

        Returns:
            arg_type: next command_iter(s) converted

        Raises:
            InputError: Argument of the wrong type was entered.
        """

        next_arg = next(command_iter)
        try:
            return arg_type(next_arg)
        except TypeError and ValueError:
            raise InputError(
                " ".join([
                    f"Sorry, '{next_arg}' needs to be of type",
                    f"'{arg_type().__class__.__name__}'",
                ])
            ) 


    def organise_args(self, command_word:str, command_iter:iter) -> list:
        """
        Organises compulsory arguments needed for given command word.

        Args:
            command_word (str): The command word
            command_iter (iter): The iterable arguments from the input

        Raises:
            InputError: Raised if insufficient arguments are given

        Returns:
            list: The arguments, 
            formatted so to be used in command functions.
        """
        args = list()
        try:
            command_args = self.command_dict[command_word]["args"]
        except KeyError:
            command_args = []
        for arg_type in command_args:
            try:
                new_arg = self.convert_command_args(arg_type, command_iter)
                args.append(new_arg)
            except StopIteration:
                raise InputError(
                    "".join([
                        f"Sorry, '{command_word}' needs ",
                        f"{len(command_args)} arguments."
                    ])
                )
        return args


    def organise_opt(self, command_word:str, command_iter:iter) -> list:
        """
        Organises optional arguments needed for given command word.

        Args:
            command_word (str): The command word.
            command_iter (iter): The iterable arguments from the input.

        Returns:
            list: The optional arguments, 
            formatted so to be used in command functions.
        """
        args = list()
        try:
            command_opt = self.command_dict[command_word]["optional"]
        except KeyError:
            command_opt = []
        for arg_type in command_opt:
            try:
                new_arg = self.convert_command_args(arg_type, command_iter)
                args.append(new_arg)
            except StopIteration or InputError:
                ... 
        return args


    def overflow_arg(self, command_iter:iter) -> None:
        """
        Checks if there's too many arguments in the given input.

        Args:
            command_iter (iter): The supposedly empty iterator.

        Raises:
            InputError: Raised if command_iter isn't empty.
        """
        try:
            next(command_iter) 
        except StopIteration:
            return
        raise InputError("Sorry, You have too many arguments.")


    def get_tags(self, command:list) -> tuple:
        """        
        Gets tags for the specific command word and remove them
        from the command input list, and set those tags to true.

        Args:
            command (list[str]): contains command word and args.

        Returns:
            tuple[list[str], dict[str,bool]]: the modified command 
            list and a dict of True boolean tags.
        """
        try:
            command_tags = self.command_dict[command[0].upper()]["tags"]
        except KeyError:
            return command, None

        tags = dict()
        for word in command[1:]:
            for tag in command_tags:
                if tag == word.lower():
                    tags[tag] = True
                    command.remove(word)
        return command, [(tag,True) for tag in tags.keys()]


    def command_valid(self, command:list) -> list:
        """
        Checks if the input is valid and
        creates the correct arguments via other methods.

        Args:
            command (list[str]): contains a command then arguments as strings.

        Returns:
            list[str]: contains a valid uppercase command 
                       and the necessary arguments in their correct types
                       if the input was valid.
        """
        self.command_word_valid(command)

        command, tags = self.get_tags(command)

        command_iter = iter(command[1:])

        args = self.organise_args(command[0].upper(), command_iter)\
             + self.organise_opt(command[0].upper(), command_iter)

        self.overflow_arg(command_iter)
        return [command[0]] + args + (tags if tags != None else [])


    def get_command(self) -> tuple:
        """
        Gets formatted command from a user input

        Returns:
            tuple[list,str]: 
                list: Command_name, *args for that command.
                str: Raw input.
        """
        command_str = input()
        command = self.command_valid(command_str.strip().split(" "))
        
        return [command[0], *command[1:]] \
                if len(command) > 1 else command, command_str
    
    
