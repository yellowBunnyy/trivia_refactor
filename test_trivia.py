import pytest
from trivia import Game, GameQuestion
from trivia import NotEnoughPlayer, MaximumPlayerLimitExceededException


@pytest.fixture
def questions():
    questions = GameQuestion()
    return questions


@pytest.fixture
def game_with_one_player(questions):
    game = Game(questions)
    game.add_player("Chet")
    return game


@pytest.fixture
def game_with_more_than_one_player(questions):
    game = Game(questions)
    game.add_player("Chet")
    game.add_player("Pat")
    game.add_player("Sue")
    return game


def test_created_questions_should_return_filled_question_lists():
    question_limit = 50
    questions = GameQuestion()
    questions.question_limit = question_limit
    for list_with_questions in [
        questions.question_container["Pop"],
        questions.question_container["Sciences"],
        questions.question_container["Sports"],
        questions.question_container["Rock"],
    ]:
        assert len(list_with_questions) == question_limit


def test_how_many_question_have_in_mostly_asked_category_should_return_false_if_we_dont_have_questions(
    questions,
):
    questions.question_container["Pop"] = ["q1", "q2", "q3"]
    questions.question_container["Rock"] = ["q1", "q2", "q3"] * 2
    questions.question_container["Sports"] = ["q1", "q2", "q3"] * 3
    questions.question_container["Sciences"] = []
    assert not questions.have_enough_questions


def test_how_many_question_have_in_mostly_asked_category_should_return_true_if_we_have_questions(
    questions,
):
    questions.question_container["Pop"] = ["q1", "q2", "q3"]
    questions.question_container["Rock"] = ["q1", "q2", "q3"] * 2
    questions.question_container["Sports"] = ["q1", "q2", "q3"] * 3
    questions.question_container["Sciences"] = ["q1", "q2", "q3"]
    assert questions.have_enough_questions


def test_add_player_to_game_should_append_player(game_with_one_player):
    assert game_with_one_player.how_many_players == 1
    assert game_with_one_player.players[0] == "Chet"
    assert not game_with_one_player.in_penalty_box[0]


def test_add_max_amount_player_should_all_players(questions):
    game = Game(questions)
    players = ("a", "b", "c", "d", "e", "f")

    for player in players:
        game.add_player(player)

    assert game.how_many_players == len(players)


def test_add_more_player_than_max_limit_should_raise_exception():
    game = Game(questions)
    players = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k")

    with pytest.raises(MaximumPlayerLimitExceededException):
        for player in players:
            game.add_player(player)


def test_check_if_more_than_one_player_should_return_true(
    game_with_more_than_one_player,
):
    assert game_with_more_than_one_player.is_playable() == True


def test_not_enough_players_shoud_raise_exception(questions):
    game = Game(questions)
    game.add_player("Norman")
    with pytest.raises(NotEnoughPlayer):
        game.is_playable()


def test_player_move_should_return_seted_place_in_places(
    game_with_more_than_one_player,
):
    dice_role = 3
    game_with_more_than_one_player.player_move(dice_role)
    assert game_with_more_than_one_player.places[0] == 3


def test_get_category_question_should_return_question_category(
    game_with_more_than_one_player,
):
    dice_roll = 3
    game_with_more_than_one_player.get_category_question(dice_roll)
    assert game_with_more_than_one_player.current_category == "Rock"


def test_get_question_should_print_question(game_with_more_than_one_player):
    category = "Pop"
    game_with_more_than_one_player.current_category = category
    result = game_with_more_than_one_player.ask_question()
    assert result == "Pop Question 0"


def test_add_coin_to_player_should_return_1(game_with_more_than_one_player):
    game_with_more_than_one_player.add_coin_to_player()
    assert game_with_more_than_one_player.purses[0] == 1


def test_go_to_next_player_should_return_next_player(game_with_more_than_one_player):
    game_with_more_than_one_player.go_to_next_player()
    current_player_index = game_with_more_than_one_player.current_player
    assert game_with_more_than_one_player.players[current_player_index] == "Pat"


def test_go_to_next_player_when_we_are_in_last_player_position_should_return_first_player(
    game_with_more_than_one_player,
):
    game_with_more_than_one_player.current_player = 2
    game_with_more_than_one_player.go_to_next_player()
    assert (
        game_with_more_than_one_player.players[
            game_with_more_than_one_player.current_player
        ]
        == "Chet"
    )


def test_was_correct_answer_if_is_should_add_coin_to_player(
    game_with_more_than_one_player,
):
    game_with_more_than_one_player.was_correctly_answered()
    assert game_with_more_than_one_player.purses[0] == 1
    assert game_with_more_than_one_player.current_player == 1


def test_was_corret_answer_but_player_have_penalty_flag_should_go_to_next_player_without_adding_coin(
    game_with_more_than_one_player,
):
    game_with_more_than_one_player.in_penalty_box[0] = True
    game_with_more_than_one_player.was_correctly_answered()
    assert game_with_more_than_one_player.purses[0] == 0
    assert game_with_more_than_one_player.current_player == 1


def test_did_player_win_shuld_set_winner_flag_to_true(game_with_more_than_one_player):
    game_with_more_than_one_player.purses[0] = 6
    game_with_more_than_one_player.did_player_win()
    assert game_with_more_than_one_player.have_winner


def test_did_player_win_should_return_false_if_does_not(game_with_more_than_one_player):
    game_with_more_than_one_player.did_player_win()
    assert not game_with_more_than_one_player.have_winner


def test_is_draw_should_return_true_if_we_dont_have_questions_in_mostly_asked_category(
    game_with_more_than_one_player,
):
    game_with_more_than_one_player.questions.question_container = {
        "Pop": ["q1", "q2", "q3"],
        "Rock": ["q1", "q2", "q3"] * 2,
        "Sports": ["q1", "q2", "q3"] * 3,
        "Sciences": [],
    }
    assert game_with_more_than_one_player.is_draw


def test_is_draw_should_return_None_if_we_have_questions(
    game_with_more_than_one_player,
):
    assert not game_with_more_than_one_player.is_draw
