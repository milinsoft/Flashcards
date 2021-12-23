class Flashcards:
    flashcards = dict()

    def __init__(self, number_of_cards: int):
        self.number_of_cards = number_of_cards

    def create_flashcards(self):
        def get_term() -> str:
            _term = input(f"The term for card #{n}:\n")
            while _term in self.flashcards:
                print(f'The term "{_term}" already exists. Try again:')
                _term = input()
            return _term

        def get_definition() -> str:
            _definition = input(f"The definition for card #{n}:\n")
            while _definition in self.flashcards.values():
                print(f"The definition \"{_definition}\" already exists. Try again:")
                _definition = input()
            return _definition

        for n in range(1, self.number_of_cards + 1):
            term = get_term()
            definition = get_definition()
            self.flashcards[term] = definition

    def get_key_by_value(self, _value: str) -> str:
        _items_list = list(self.flashcards.items())
        for _item in _items_list:
            if _value in _item:
                return _item[0]

    def test_user_knowledge(self):
        for card in self.flashcards.keys():
            print(f"Print the definition of \"{card}\":")
            response = input()
            if response == self.flashcards[card]:
                print("Correct!")
            else:
                if response not in self.flashcards.values():
                    print(f"Wrong. The right answer is \"{self.flashcards[card]}\"")
                else:
                    matching_key = self.get_key_by_value(response)
                    print(f"Wrong. The right answer is \"{self.flashcards[card]}\", but your definition is correct for \"{matching_key}\".")


def main():
    try:
        number_of_cards = int(input("Input the number of cards:\n"))
    except ValueError:
        print("ONLY integers allowed. try again:\n")
        return main()
    flashcards = Flashcards(number_of_cards)
    flashcards.create_flashcards()
    flashcards.test_user_knowledge()


if __name__ == '__main__':
    main()
