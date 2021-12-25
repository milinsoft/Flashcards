import pickle
import random
from io import StringIO



class Logger:
    def __init__(self):
        self.logger = StringIO()

    # working function
    def logged_input(self, input_message=""):
        _in = "\u21A9"  # char for ↩
        _out = "\u21AA"  # chars for ↪
        _input = input(f"{input_message}")
        self.logger.write(f"{_out} {''.join(input_message)}\n")
        self.logger.write(f"{_in} {str(_input)}\n")
        return _input

    # think about utilizing that as method without printing itself
    def logged_print(self, _text=""):
        _out = "\u21AA"  # chars for ↪
        self.logger.write(f"{_out} {_text}\n")
        return print(_text)


    def save_logs(self):
        logger_file = logger.logged_input("File name:\n")
        #with open("/Users/aleksander/Desktop/test.txt", "w") as log_file:
        with open(logger_file, "w") as log_file:
            for line in self.logger.getvalue():
                log_file.write(line)
        print("The log has been saved.")



class Flashcards:
    flashcards = dict()

    def __init__(self):
        self.number_of_cards = 0
 

    def create_flashcards(self):

        def get_term() -> str:
            _term = logger.logged_input(f"The term for card #{self.number_of_cards + 1}:\n")
            while _term in self.flashcards:
                logger.logged_print(f'The term "{_term}" already exists. Try again:')
                _term = logger.logged_input()
            return _term

        def get_definition() -> str:
            _definition = logger.logged_input(f"The definition for card #{self.number_of_cards + 1}:\n")
            while _definition in self.flashcards.values():
                logger.logged_print(f"The definition \"{_definition}\" already exists. Try again:")
                _definition = logger.logged_input()
            return _definition

        term = get_term()
        definition = get_definition()
        self.flashcards[term] = definition
        logger.logged_print(f"The pair (\"{term}\":\"{definition}\") has been added.")
        self.number_of_cards += 1

    def get_key_by_value(self, _value: str) -> str:
        _items_list = list(self.flashcards.items())
        for _item in _items_list:
            if _value in _item:
                return _item[0]

    def test_user_knowledge(self):
        card = random.choice([x for x in self.flashcards.keys()])
        logger.logged_print(f"Print the definition of \"{card}\":")
        response = logger.logged_input()
        if response == self.flashcards[card]:
            logger.logged_print("Correct!")
        else:
            if response not in self.flashcards.values():
                logger.logged_print(f"Wrong. The right answer is \"{self.flashcards[card]}\"")
            else:
                matching_key = self.get_key_by_value(response)
                logger.logged_print(
                    f"Wrong. The right answer is \"{self.flashcards[card]}\", but your definition is correct for \"{matching_key}\".")

    def remove_card(self):
        card_to_remove = logger.logged_input("Which card?\n")
        try:
            del self.flashcards[card_to_remove]
            logger.logged_print("The card has been removed.")
        except KeyError:
            logger.logged_print(f"Can't remove \"{card_to_remove}\": there is no such card.")

    def cards_from_file(self):
        file_name = logger.logged_input("File name:\n")
        try:
            with open(file_name, "rb") as file:
                self.flashcards = pickle.load(file)
                logger.logged_print(f"{len(self.flashcards)} cards have been loaded." if len(
                    self.flashcards) != 1 else "1 Card has been loaded.")
        except FileNotFoundError:
            logger.logged_print("File not found.")

    def store_flashcards(self):
        file_name = logger.logged_input("File name:\n")
        if not file_name.endswith(".txt"):
            logger.logged_print("Incorrect file_name, please enter something like cards.txt ")
            return self.store_flashcards()
        else:
            with open(file_name, "wb") as file:
                pickle.dump(self.flashcards, file, pickle.HIGHEST_PROTOCOL)
                logger.logged_print(f"{len(self.flashcards)} cards have been saved." if len(
                    self.flashcards) != 1 else "1 Card has been saved.")

    def reset_stats(self):
        ...


    def get_hardest_card(self):
        pass

    def menu(self):
        while True:
            # action = logger.logged_input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
            action = logger.logged_input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
            # match - case works only starting from Python 3.10 and newer
            match action:
                case 'exit':
                    logger.logged_print("bye bye")
                    logger.logger.close()  # closing loger / output object.
                    exit()
                case "add":
                    self.create_flashcards()
                case "remove":
                    self.remove_card()
                case "import":
                    self.cards_from_file()
                case "export":
                    self.store_flashcards()
                case "ask":
                    try:
                        repeat = int(logger.logged_input("How many times to ask?\n"))
                        for _ in range(repeat):
                            self.test_user_knowledge()
                    except ValueError:
                        logger.logged_print("Print natural number (integer)")

                case "log":
                    logger.save_logs()

                case "hardest card":
                    self.get_hardest_card()

                case "reset stats":
                    self.reset_stats()


                case _:
                    logger.logged_print("Incorrect option. Try again:")
                    return self.menu()


if __name__ == '__main__':
    logger = Logger()
    flashcards = Flashcards()
    flashcards.menu()


# HINT
""" 
The hardest part it's probably the logger. I used the hints, it wasn't easy but in the end i figured out. What i was missing is the correct usage of StringIO object.

you can create the StringIO object, after importing from io module, with:
mem_buffer = StringIO()

after that every time you want to write something in memory, you can do:
mem_buffer.write('some_string\n')
for me, i had to add the '\n' at the end every time, tried some argument like "newline='\n'" when i declared the constructor, but it didn't work. 

Anyway, the part that is missing from the previous hint and that caused me some trouble is the reading part. When you have to read the content previously written there are 2 ways:

- using mem_buffer.getvalue() that return all the content of the buffer

- use mem_buffer.seek(0) to set the pointer at the beginning and mem_obj.read() to read the contents.

After reading all the contents you can use the context manager or the function open to write on file what you have read. (don't forget to close the buffer in the end)

To avoid to print on console and write in the buffer i used a function:

def print_and_log(string):
    if string is not None:
        memory_file.write(string+'\n')
        print(string)

The "None" condition could not be necessary for you.

Hope it will help"""
