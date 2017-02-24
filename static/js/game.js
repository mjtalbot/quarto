class Game {
    constructor(game_uuid, player_a, player_b, events) {
        this.game_uuid = game_uuid;
        this.player_a = null;
        this.player_b = null;
        this.evetns = [];
        if (player_a !== null){
            this.player_a = new Player(player_a.name);
        }
        if (player_b !== null){
            this.player_b = new Player(player_b.name);
        }
        if (events !== null){

        }
        this.board = new Board();
    }
}

class Player {
    constructor(name) {
        this.name = name;
    }
}

class Event {
    constructor() {}
}

class Board {
    constructor() {}
}
