import unittest
from io import StringIO
from unittest import mock
from test_base import captured_io
from command_handling.commands import Commands
from command_handling.command_handling import CommandHandler
from command_handling.input_exceptions import InputError


class TestCommandHandler(unittest.TestCase):
    cmd = Commands()
    handler = CommandHandler(cmd.command_dict)


    def test_command_word_valid(self):
        #shouldn't raise error
        for key in self.handler.command_dict:
            self.handler.command_word_valid(
                [f"{key}"])
            self.handler.command_word_valid(
                [f"{key[0].lower()}{key[1:len(key)-1]}{key[-1].lower()}"])
            self.handler.command_word_valid(
                [f"{key[0]}{key[1:len(key)-1].lower()}{key[-1]}"])
            self.handler.command_word_valid(
                [f"{key.lower()}"])
        #should raise error
        try:
            self.handler.command_word_valid(["Fail"])
        except InputError as e:
            self.assertEqual("Sorry, I did not understand 'Fail'.", str(e))


    def test_convert_command_args(self):
        for key in self.handler.command_dict:
            input_args = list().copy()
            try:
                args = self.handler.command_dict[key]['args']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args_iter = iter(map(str,input_args))
            #shouldn't give an error
            if args != []:
                for i in range(len(input_args)):
                    self.assertEqual(
                        input_args[i],
                        self.handler.convert_command_args(args[i], input_args_iter))
        #now with type error
        for key in self.handler.command_dict:
            input_args = list().copy()
            try:
                args = self.handler.command_dict[key]['args']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(float())
            input_args_iter = iter(map(str,input_args))
            #shouldn't give an error
            if args != []:
                for i in range(len(input_args)):
                    try:
                        self.assertEqual(
                            input_args[i],
                            self.handler.convert_command_args(args[i], input_args_iter))
                    except InputError as e:
                        #caught an error
                        self.assertTrue(True)
                    else:
                        self.assertTrue(False)


    def test_organise_args(self):
        for key in self.handler.command_dict:
            input_args = list().copy()
            try:
                args = self.handler.command_dict[key]['args']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args_iter = iter(map(str, input_args))
            #shouldn't give an error
            self.assertEqual(
                self.handler.organise_args(key, input_args_iter),
                input_args
            )
        for key in self.handler.command_dict:
            input_args = list().copy()
            try:
                args = self.handler.command_dict[key]['args']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args_iter = iter(map(str, input_args))
            #should give an error
            if args != []:
                next(input_args_iter)
                try:
                    self.handler.organise_args(key, input_args_iter)
                except InputError as e:
                    #caught an error
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)


    def test_organise_opt(self):
        for key in self.handler.command_dict:
            input_args = list().copy()
            try:
                args = self.handler.command_dict[key]['opt']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args_iter = iter(map(str, input_args))
            #shouldn't give an error
            self.assertEqual(
                self.handler.organise_opt(key, input_args_iter),
                input_args if key!='REPLAY' else []
            )
        for key in self.handler.command_dict:
            input_args = list().copy()
            try:
                args = self.handler.command_dict[key]['opt']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args_iter = iter(map(str, input_args))
            #shouldnt give an error
            if args != []:
                next(input_args_iter)
                self.handler.organise_opt(key, input_args_iter)
        for key in self.handler.command_dict:
            input_args = list().copy()
            try:
                args = self.handler.command_dict[key]['opt']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args.append("Extra")
            input_args_iter = iter(map(str, input_args))
            #should give an error
            if args != []:
                try:
                    self.handler.organise_opt(key, input_args_iter)
                except InputError as e:
                    #caught an error
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)           


    def test_overflow_arg(self):
        try:
            self.handler.overflow_arg(iter([1]))
        except InputError as e:
            self.assertEqual(str(e), "Sorry, You have too many arguments.")
        self.handler.overflow_arg(iter([]))


    @mock.patch.object(CommandHandler, "command_word_valid")
    @mock.patch.object(CommandHandler, "organise_args")
    @mock.patch.object(CommandHandler, "organise_opt")
    @mock.patch.object(CommandHandler, "overflow_arg")
    def test_command_valid(self, *mock):
        self.handler.command_valid(["OfF"])
        for m in mock:
            m.assert_called()


    def test_get_command(self):
        for key in ["LEFT", "RIGHT", "HELP", "REPLAY", "OFF"]:
            input_string = "Fail\n"
            input_string += f"{key}\n"
            input_string += f"{key.lower()}\n"
            input_string += f"{key[0]}{key[1:len(key)-1].lower()}{key[-1]}\n"
            input_string += f"{key[0].lower()}{key[1:len(key)-1]}{key[-1].lower()}\n"

            with captured_io(StringIO(input_string)) as (out, err):
                try:
                    self.handler.get_command()
                except InputError as e:
                    self.assertEqual("Sorry, I did not understand 'Fail'.", str(e))
                for _ in range(4):
                    self.assertEquals(self.handler.get_command()[0][0].upper(), key)


if __name__ == '__main__':
    unittest.main()