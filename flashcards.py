import pickle
import random
from io import StringIO



class Logger:
    def __init__(self):
        self.logger = StringIO()

    # working function
    def logged_input(self, prompt=""):
        _in = "\u21A9"  # char for ↩
        _out = "\u21AA"  # chars for ↪
        _input = input(prompt)
        self.logger.write(f"{_out} {''.join(prompt)}\n")
        self.logger.write(f"{_in} {str(_input)}\n")
        return _input

    # think about utilizing that as method without printing itself
    def print_and_log(self, *args, **kwargs):
        _out = "\u21AA"  # chars for ↪
        # print to sys.stdout
        print(*args, **kwargs)
        # print to log file
        #print(f"{_out} ", file=self.logger)
        print(_out, *args, **kwargs, file=self.logger)  # ato



    def save_logs(self):
        logger_file = logger.logged_input("File name:\n")
        #with open("/Users/aleksander/Desktop/test.txt", "w") as log_file:
        with open(logger_file, "w") as log_file:
            for line in self.logger.getvalue():
                log_file.write(line)
        print("The log has been saved.")



class Flashcards:
    flashcards = dict()
    mistakes = dict()

    def __init__(self):
        self.number_of_cards = 0
 

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
        self.mistakes.setdefault(term, 0)

        logger.print_and_log(f"The pair (\"{term}\":\"{definition}\") has been added.")
        self.number_of_cards += 1

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
            if response not in self.flashcards.values():
                self.mistakes[card] += 1
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
        file_name = logger.logged_input("File name:\n")
        try:
            with open(file_name, "rb") as file:
                self.flashcards = pickle.load(file)
                logger.print_and_log(f"{len(self.flashcards)} cards have been loaded." if len(
                    self.flashcards) != 1 else "1 Card has been loaded.")
        except FileNotFoundError:
            logger.print_and_log("File not found.")

    def store_flashcards(self):
        file_name = logger.logged_input("File name:\n")
        if not file_name.endswith(".txt"):
            logger.print_and_log("Incorrect file_name, please enter something like cards.txt ")
            return self.store_flashcards()
        else:
            with open(file_name, "wb") as file:
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
            action = logger.logged_input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
            # match - case works only starting from Python 3.10 and newer
            match action:
                case 'exit':
                    print("bye bye")
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
    logger = Logger()
    flashcards = Flashcards()
    flashcards.menu()
