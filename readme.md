# Quarto

Simple game that lets you play quarto. well it lets a computer play really, there's hardly a way to let you play, but its good enough for me. good enough for me.

# Todo:
- UI:
    - enhance ui
    - add in bower
    - show games youre in
- Websockets
    - deal with errors over websockets
    - invites to join a game
- Backend:
    - add a lobby (mostly for ai's)
    - show games
        - open, closed, finished based on who's in them
    - invite players to join (email or ai player name??)
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
    @returns json dump of game state. (board, moves, all that shit)

# Place a piece
    POST /game/quarto/<game_id>/placement_move
    @param player_name
    @param x
    @param y
    @returns json dump of game state. (board, moves, all that shit)
