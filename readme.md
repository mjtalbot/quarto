# Quarto

Simple game that lets you play quarto. well it lets a computer play really, there's hardly a way to let you play, but its good enough for me. good enough for me.

# Todo:

- UI:
    - represent game in front end
        - allow making moves
        - make display for a game (uuid, player names, pieces and board)
        - show winner (could get returned with the game when its won?)
    - enhance ui
    - add in bower
- Backend:
    - list closed games
    - list open games
    - list games you're in
    - invite players to join (email or ai player name??)
    - websocket support
- General:
    create setup.py
    create an AI to play players if requested
- Deploy
    Autodeploy on master push

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
