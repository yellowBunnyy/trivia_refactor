#!/usr/bin/env python3
from abc import ABC


class BaseGameExeceptions(Exception):
    pass


class MaximumPlayerLimitExceededException(BaseGameExeceptions):
    pass


class NotEnoughPlayer(BaseGameExeceptions):
    pass


class GameQuestionInterface(ABC):
    def create_questions(self) -> None:
        raise NotImplemented()

    def create_rock_question(self) -> str:
        raise NotImplemented()


class GameQuestion(GameQuestionInterface):
    def __init__(self) -> None:
        self.question_container = {"Pop": [], "Sciences": [], "Sports": [], "Rock": []}
        self.question_limit = 50
        self.create_questions()

    def create_questions(self) -> None:
        for i in range(self.question_limit):
            self.question_container["Pop"].append(f"Pop Question {i}")
            self.question_container["Sciences"].append(f"Science Question {i}")
            self.question_container["Sports"].append(f"Sports Question {i}")
            self.question_container["Rock"].append(self.create_rock_question(i))

    def create_rock_question(self, index: int) -> str:
        return f"Rock Question {index}"

    @property
    def have_enough_questions(self):
        return all([len(questions) for _, questions in self.question_container.items()])


class Game:

    category = {
        "Pop": [0, 4, 8],
        "Sciences": [1, 5, 9],
        "Sports": [2, 6, 10],
        "Rock": [3, 7, 11],
    }

    def __init__(self, game_questions: GameQuestionInterface, max_player: int = 6):
        self.max_player = max_player
        self.questions = game_questions
        self.players = []
        self.places = [0] * self.max_player
        self.purses = [0] * self.max_player
        self.in_penalty_box = [0] * self.max_player
        self.points_to_win = 6

        self.current_category = None
        self.current_player = 0
        self.have_winner = False

    @property
    def how_many_players(self) -> int:
        return len(self.players)

    def add_player(self, player: str) -> None:
        if self.how_many_players > self.max_player:
            raise MaximumPlayerLimitExceededException(
                "Max player limit has been reached!"
            )
        self.players.append(player)
        self.adding_player_printer(player=player)

    def adding_player_printer(self, player: str) -> None:
        print(player + " was added")
        print(f"They are player number {self.how_many_players}")

    def roll(self, roll: int) -> None:
        self.is_playable()
        print(f"{self.players[self.current_player]} is the current player.")
        print(f"They have rolled a {roll}")

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                print(
                    f"{self.players[self.current_player]} is getting out of the penalty box"
                )
                self.player_move(roll)
                
            else:
                print(
                    f"{self.players[self.current_player]} is not getting out of the penalty box"
                )
                self.is_getting_out_of_penalty_box = False
        else:
            self.player_move(roll=roll)
            

    def is_playable(self) -> bool:
        if self.how_many_players < 2:
            raise NotEnoughPlayer
        return True

    def player_move(self, roll: int) -> str:
        self.places[self.current_player] = self.places[self.current_player] + roll
        if self.places[self.current_player] > 11:
            self.places[self.current_player] = self.places[self.current_player] - 12
        print(
            f"{self.players[self.current_player]}'s new location is {self.places[self.current_player]}"
        )
        self.get_category_question(dice_roll=roll)

    def get_category_question(self, dice_roll: int) -> None:
        _category = next(
            category for category, nums in self.category.items() if dice_roll in nums
        )
        self.current_category = _category
        print(f"The category is {self.current_category}")
        self.ask_question()

    def ask_question(self) -> str:
        return self.questions.question_container[self.current_category].pop(0)

    def was_correctly_answered(self) -> None:
        if self.in_penalty_box[self.current_player]:
            self.go_to_next_player()
            self.in_penalty_box[self.current_player] = False
        else:
            self.add_coin_to_player()

    def go_to_next_player(self) -> None:
        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0

    def add_coin_to_player(self) -> None:
        self.purses[self.current_player] += 1
        _message = " ".join(
            [
                self.players[self.current_player],
                "now has",
                f"{self.purses[self.current_player]}",
                "Gold Coins.",
            ]
        )
        print(_message)
        self.did_player_win()
        self.go_to_next_player()

    def did_player_win(self) -> bool:
        if self.points_to_win in self.purses:
            print("winner!")
            self.have_winner = True
        return False

    @property
    def is_draw(self) -> bool:
        if not self.questions.have_enough_questions:
            print("We don't have questions!!! Is Draw.")
            return True

    def wrong_answer(self) -> None:
        _message = " ".join(
            [
                "Question was incorrectly answered",
                f"{self.players[self.current_player]}",
                "was sent to the penalty box",
            ]
        )
        print(_message)
        self.in_penalty_box[self.current_player] = True
        self.go_to_next_player()


from random import randrange

if __name__ == "__main__":
    questions = GameQuestion()
    game = Game(questions)

    game.add_player("Chet")
    game.add_player("Pat")
    game.add_player("Sue")
    while True:
        game.roll(randrange(1, 7))

        if randrange(9) == 7:
            game.wrong_answer()
        else:
            game.was_correctly_answered()

        if game.have_winner or game.is_draw:
            break
