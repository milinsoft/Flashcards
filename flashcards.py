import pickle
import random


class Flashcards:
    flashcards = dict()

    def __init__(self):
        self.number_of_cards = 0

    def create_flashcards(self):

        def get_term() -> str:
            _term = input(f"The term for card #{self.number_of_cards + 1}:\n")
            while _term in self.flashcards:
                print(f'The term "{_term}" already exists. Try again:')
                _term = input()
            return _term

        def get_definition() -> str:
            _definition = input(f"The definition for card #{self.number_of_cards + 1}:\n")
            while _definition in self.flashcards.values():
                print(f"The definition \"{_definition}\" already exists. Try again:")
                _definition = input()
            return _definition

        term = get_term()
        definition = get_definition()
        self.flashcards[term] = definition
        print(f"The pair (\"{term}\":\"{definition}\") has been added.")
        self.number_of_cards += 1

    def get_key_by_value(self, _value: str) -> str:
        _items_list = list(self.flashcards.items())
        for _item in _items_list:
            if _value in _item:
                return _item[0]

    def test_user_knowledge(self):
        card = random.choice([x for x in self.flashcards.keys()])
        print(f"Print the definition of \"{card}\":")
        response = input()
        if response == self.flashcards[card]:
            print("Correct!")
        else:
            if response not in self.flashcards.values():
                print(f"Wrong. The right answer is \"{self.flashcards[card]}\"")
            else:
                matching_key = self.get_key_by_value(response)
                print(
                    f"Wrong. The right answer is \"{self.flashcards[card]}\", but your definition is correct for \"{matching_key}\".")

    def remove_card(self):
        card_to_remove = input("Which card?\n")
        try:
            del self.flashcards[card_to_remove]
            print("The card has been removed.")
        except KeyError:
            print(f"Can't remove \"{card_to_remove}\": there is no such card.")

    def cards_from_file(self):
        file_name = input("File name:\n")
        try:
            with open(file_name, "rb") as file:
                self.flashcards = pickle.load(file)
                print(f"{len(self.flashcards)} cards have been loaded." if len(
                    self.flashcards) != 1 else "1 Card has been loaded.")
        except FileNotFoundError:
            print("File not found.")

    def store_flashcards(self):
        file_name = input("File name:\n")
        if not file_name.endswith(".txt"):
            print("Incorrect file_name, please enter something like cards.txt ")
            return self.store_flashcards()
        else:
            with open(file_name, "wb") as file:
                pickle.dump(self.flashcards, file, pickle.HIGHEST_PROTOCOL)
                print(f"{len(self.flashcards)} cards have been saved." if len(
                    self.flashcards) != 1 else "1 Card has been saved.")

    def menu(self):
        while True:
            action = input("Input the action (add, remove, import, export, ask, exit):\n")
            if action == 'exit':
                print("bye bye")
                exit()
            elif action == "add":
                self.create_flashcards()
            elif action == "remove":
                self.remove_card()
            elif action == "import":
                self.cards_from_file()
            elif action == "export":
                self.store_flashcards()
            elif action == "ask":
                repeat = int(input("How many times to ask?\n"))
                for _ in range(repeat):
                    self.test_user_knowledge()
            else:
                print("Incorrect option. Try again:")
                return self.menu()


if __name__ == '__main__':
    flashcards = Flashcards()
    flashcards.menu()
