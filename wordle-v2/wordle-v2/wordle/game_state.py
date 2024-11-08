
class GameState:

	ERROR = 0
	OK = 1<<0
	END_WIN = 1<<1
	END_LOSS = 1<<2
	ENDED = END_WIN | END_LOSS
	INVALID_WORD = 1<<3
	TOO_FEW_LETTERS = 1<<4



