class Flashcards:
    flashcards = dict()

    def __init__(self, number_of_cards):
        self.number_of_cards = number_of_cards

    def create_flashcards(self):
        for n in range(1, self.number_of_cards + 1):
            term = input(f"The term for card #{n}:\n")
            definition = input(f"The definition for card #{n}:\n")
            self.flashcards[term] = definition

    def test_user_knowledge(self):
        for card in self.flashcards.keys():
            print(f"Print the definition of \"{card}\":")
            response = input()
            print("Correct!" if response == self.flashcards[card] else f"Wrong. The right answer is \"{self.flashcards[card]}\"")


def main():
    number_of_cards = int(input("Input the number of cards:\n"))
    flashcards = Flashcards(number_of_cards)
    flashcards.create_flashcards()
    flashcards.test_user_knowledge()


if __name__ == '__main__':
    main()
