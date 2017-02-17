# Quarto

Simple game that lets you play quarto. well it lets a computer play really, there's hardly a way to let you play, but its good enough for me. good enough for me.

# Todo:

- make a main, (maybe where you can play command line style? well.. maybe not)

- make a setup
- allow for this game to be importable. storable and loadable
- make game host
    - load games from file on demand (turn by turn i guess???)
    - games get an id.
    - store and load by id.
    - func to get all the game
    - websockets to tie into the game "live" as you wish...
    - hopefully playing through the game each move is fast enough.. we'll see i guess.. but that should mean we dont have to keep anything much in memory.

# API

# Create Game
    POST /game/quarto/
    @param player_name
    @param public (not implemented)
    @returns game_id

# Join Game
    POST /game/quarto/<game_id>/join
    @param player_name

# Get Game State
    GET /game/quarto/<game_id>
    @returns json dump of game state. (board, moves, all that shit)

# Pick a piece
    POST /game/quarto/<game_id>/picking_move
    @param player_name
    @param number

# Place a piece
    POST /game/quarto/<game_id>/placement_move
    @param player_name
    @param x
    @param y



# Websockets

# up register Available to play
# up give game state

# down you're in game with id
# down move & state for game with id
# down you're move
# down game ids you're playing in


# rest api to get games your in. 
