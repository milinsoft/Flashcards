import pickle
import random
from io import StringIO
import argparse


class Logger:
    def __init__(self):
        self.logger = StringIO()

    # working function
    def logged_input(self, prompt=""):
        _in = "\u21A9"  # char for ↩
        _out = "\u21AA"  # chars for ↪
        _input = input(prompt)
        self.logger.write(f"{_out} {''.join(prompt)}\n{_in} {str(_input)}\n")
        return _input

    # think about utilizing that as method without printing itself
    def print_and_log(self, *args, **kwargs):
        _out = "\u21AA"  # chars for ↪
        # print to sys.stdout
        print(*args, **kwargs)
        # print to log file
        print(_out, *args, **kwargs, file=self.logger)  # ato

    def save_logs(self):
        logger_file = logger.logged_input("File name:\n")
        with open(logger_file, "w") as log_file:
            for line in self.logger.getvalue():
                log_file.write(line)
        print("The log has been saved.")


class Flashcards:
    flashcards = dict()
    mistakes = dict()

    def __init__(self, import_file=None, export_file=None):
        self.number_of_cards = 0
        self.import_file = import_file
        self.export_file = export_file

    def create_flashcards(self):

        def get_term() -> str:
            _term = logger.logged_input(f"The term for card #{self.number_of_cards + 1}:\n")
            while _term in self.flashcards:
                logger.print_and_log(f'The term "{_term}" already exists. Try again:')
                _term = logger.logged_input()
            return _term

        def get_definition() -> str:
            _definition = logger.logged_input(f"The definition for card #{self.number_of_cards + 1}:\n")
            while _definition in self.flashcards.values():
                logger.print_and_log(f"The definition \"{_definition}\" already exists. Try again:")
                _definition = logger.logged_input()
            return _definition

        term = get_term()
        definition = get_definition()

        self.flashcards[term] = definition
        self.update_mistakes_count()

        logger.print_and_log(f"The pair (\"{term}\":\"{definition}\") has been added.")
        self.number_of_cards += 1

    def update_mistakes_count(self):
        for card in self.flashcards:
            self.mistakes.setdefault(card, 0)

    def get_key_by_value(self, _value: str) -> str:
        _items_list = list(self.flashcards.items())
        for _item in _items_list:
            if _value in _item:
                return _item[0]

    def test_user_knowledge(self):
        card = random.choice([x for x in self.flashcards.keys()])
        logger.print_and_log(f"Print the definition of \"{card}\":")
        response = logger.logged_input()
        if response == self.flashcards[card]:
            logger.print_and_log("Correct!")
        else:
            self.mistakes[card] += 1
            if response not in self.flashcards.values():
                logger.print_and_log(f"Wrong. The right answer is \"{self.flashcards[card]}\"")
            else:
                matching_key = self.get_key_by_value(response)
                logger.print_and_log(
                    f"Wrong. The right answer is \"{self.flashcards[card]}\", but your definition is correct for \"{matching_key}\".")

    def remove_card(self):
        card_to_remove = logger.logged_input("Which card?\n")
        try:
            del self.flashcards[card_to_remove]
            logger.print_and_log("The card has been removed.")
        except KeyError:
            logger.print_and_log(f"Can't remove \"{card_to_remove}\": there is no such card.")

    def cards_from_file(self):
        if not self.import_file:
            file_name = logger.logged_input("File name:\n")
        else:
            file_name = self.import_file
        try:
            with open(file_name, "rb") as file:
                self.flashcards = pickle.load(file)
                self.update_mistakes_count()
                logger.print_and_log(
                    f"{len(self.flashcards)} cards have been loaded.")  # if len(self.flashcards) != 1 else "1 Card has been loaded.")
        except FileNotFoundError:
            self.import_file = None
            logger.print_and_log("File not found.")

    def store_flashcards(self):
        if not self.export_file:
            self.export_file = logger.logged_input("File name:\n")

        if not self.export_file.endswith(".txt"):
            logger.print_and_log("Incorrect file_name, please enter something like cards.txt ")
            return self.store_flashcards()
        else:
            with open(self.export_file, "wb") as file:
                pickle.dump(self.flashcards, file, pickle.HIGHEST_PROTOCOL)
                logger.print_and_log(f"{len(self.flashcards)} cards have been saved." if len(
                    self.flashcards) != 1 else "1 Card has been saved.")

    def reset_stats(self):
        ...
        for key in self.mistakes:
            self.mistakes[key] = 0
        logger.print_and_log("Card statistics have been reset.")

    def get_hardest_card(self):
        if not self.mistakes:
            logger.print_and_log("There are no cards with errors.")
        else:
            self.mistakes = dict(sorted(self.mistakes.items(), key=lambda x: x[1], reverse=True))
            pair = list(self.mistakes.items())[0]
            if pair[1] > 0:
                logger.print_and_log(f"The hardest card is \"{pair[0]}\". You have {pair[1]} errors answering it.")
            else:
                logger.print_and_log("There are no cards with errors.")

    def menu(self):
        while True:
            # action = logger.logged_input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
            action = logger.logged_input(
                "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
            # match - case works only starting from Python 3.10 and newer
            match action:
                case 'exit':
                    print("bye bye")
                    if self.export_file:
                        self.store_flashcards()
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
                        logger.print_and_log("Print natural number (integer)")
                case "log":
                    logger.save_logs()
                case "hardest card":
                    self.get_hardest_card()
                case "reset stats":
                    self.reset_stats()
                case _:
                    logger.print_and_log("Incorrect option. Try again:")
                    return self.menu()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="", description="Not yet implemented")
    parser.add_argument("--import_from", type=str,
                        help="If --import_from=IMPORT is passed, where IMPORT is the file name, read the initial card set from the external file, and print the message n cards have been loaded.")
    parser.add_argument("--export_to", type=str,
                        help="If --export_to=EXPORT is passed, where EXPORT is the file name, write all cards that are in the program memory into this file after the user has entered exit, and the last line of the output should be n cards have been saved.")
    _args = parser.parse_args()

    logger = Logger()
    flashcards = Flashcards(import_file=_args.import_from, export_file=_args.export_to)

    if _args.import_from:
        flashcards.cards_from_file()

    flashcards.menu()
