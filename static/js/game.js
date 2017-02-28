class Game {
    constructor(game_uuid, player_a, player_b, winner, events) {
        this.uuid = game_uuid;
        this.player_a = null;
        this.player_b = null;
        this.winner = null;
        this.events = [];
        if (player_a){
            this.player_a = new Player(player_a.name);
        }
        if (player_b){
            this.player_b = new Player(player_b.name);
        }
        if (winner){
            this.winner = new Player(winner.name);
        }
        this.board = new Board();
        if (events){
            // e.g. {
            //     "move":{
            //         "piece":{
            //             "value":0
            //         },
            //         "type":"PickingMove"
            //     },
            //     "player":{
            //         "name":"asdf"
            //     }
            // }
            // {"move":{"type":"PlacementMove","x":2,"y":0},"player":{"name":"asdf2"}}
            events.forEach(function(item, index, array){
                this.apply_event(item);
            }.bind(this));
        }
    }
    apply_event(item){
        if (item.move.type == 'PickingMove') {
            this.board.select_piece(
                item.move.piece.value
            );
        }
        else if (item.move.type == 'PlacementMove'){
            this.board.set_piece(
                item.move.x,
                item.move.y
            );
        }
        this.events.push(item);
    }
    set_player_b(name){
        this.player_b = new Player(name);
    }
    set_winner(name){
        this.winner = new Player(name);
    }
    get_player_a(){
        if (this.player_a){
            return this.player_a.name;
        }
        return '';
    }
    get_player_b(){
        if (this.player_b){
            return this.player_b.name;
        }
        return '';
    }
    get_winner(){
        if (this.winner){
            return this.winner.name;
        }
        return '';
    }
    get_turn(){
        if (this.winner)
            return '';
        var turn_type = 'Picking';
        var player = this.get_player_a();
        if (this.events.length % 2 ==1){
            turn_type = 'Placement';
        }
        if (
            this.events.length % 4 == 1 ||
            this.events.length % 4 == 2
        ){
            player = this.get_player_b();
        }
        return `${player}'s turn to make a ${turn_type} move`;
    }
    get_svg(){
        var output = `
        <div class="row">
            <div class="col-sm-2">Game Id</div>
            <div class="col-sm-10">${this.uuid}</div>
        </div>
        <div class="row">
            <div class="col-sm-2">Playber 1</div>
            <div class="col-sm-10">${this.get_player_a()}</div>
        </div>
        <div class="row">
            <div class="col-sm-2">Playber 2</div>
            <div class="col-sm-10">${this.get_player_b()}</div>
        </div>
        <div class="row">
            <div class="col-sm-2">Winner</div>
            <div class="col-sm-10">${this.get_winner()}</div>
        </div>
        <div class="row">
            <div class="col-sm-2">Turn</div>
            <div class="col-sm-10">${this.get_turn()}</div>
        </div>
        <svg width="1200" height="700">
            <g transform="translate(250,0)">
                <g transform="rotate(30)">
                    ${this.board.get_board_svg(500)}
                </g>
            </g>
            <g transform="translate(700,0)">
                ${this.board.get_remaining_pieces_svg(300)}
            </g>
            <g transform="translate(1000,0)">
                ${this.board.get_selected_piece(100)}
            </g>
        </svg>`;

        return  output;
    }
}

class Player {
    constructor(name) {
        this.name = name;
    }
}

class Piece {
    constructor(value) {
        this.value = value;
    }
    get_circle(width, padding, hole) {
        var hole_svg = ``;
        if (hole) {
            hole_svg = this.get_circle(width, width/2 + padding/4, false);
        }
        return `
            M ${width/2} ${width - padding/2}
            A ${(width-padding)/2} ${(width-padding)/2} 0 1 1 ${width/2+0.0001} ${(width - padding/2)} z
            ${hole_svg}
        `;
    }
    get_square(width, padding, hole) {
        var hole_svg = ``;
        if (hole) {
            hole_svg = this.get_square(width, width/4 + padding/2, false);
        }
        return `
            M ${padding} ${padding}
            H ${width - padding}
            V ${width - padding}
            H ${padding}
            Z ${hole_svg}
        `;
    }
    get_piece_svg(width){
        var color = ((this.value & 1) == 1)? 'blue': 'red';
        var padding = ((this.value & 2) == 2)? 3*width/10: width/10;
        var circle = ((this.value & 4) == 4)? true: false;
        var hole = ((this.value & 8) == 8)? true: false;

        var shape = '';
        if (circle) {
            shape = this.get_circle(width, padding, hole);
        }
        else {
            shape = this.get_square(width, padding, hole);
        }

        return `<path
            class="piece"
            value="${this.value}"
            fill="${color}"
            fill-rule="evenodd"
            d="${shape}"
        />`;
    }
}

class Board {
    constructor() {
        this.available_pieces = {};
        this.selected_piece = null;
        for (var x=0; x<16; x++) {
            this.available_pieces[x] = new Piece(x);
        }
        this.positions = [];
        for (x=0; x<4; x++) {
            this.positions.push([]);
            for (var y=0; y<4; y++) {
                this.positions[x].push(null);
            }
        }
    }
    select_piece(number){
        if (this.available_pieces[number]) {
            this.selected_piece = this.available_pieces[number];
            this.available_pieces[number] = null;
        }
    }
    set_piece(x, y){
        this.positions[x][y] = this.selected_piece;
        this.selected_piece = null;
    }

    get_remaining_pieces_svg(total_width){
        var output = `<rect x="0" y="0"
            width="${total_width}" height="${total_width}"
            fill="gray"/>`;
        output += `<g id="remaining_pieces">`;
        var field_width = total_width/4;
        for (var i in this.available_pieces) {
            if (this.available_pieces[i]) {
                output += `<g transform="translate(${field_width * (i % 4)}, ${field_width * Math.floor(i / 4)})">
                    ${this.available_pieces[i].get_piece_svg(field_width)}
                </g>`;
            }
        }

        output += `</g>`;
        return output;
    }
    get_selected_piece(total_width){
        var output = `<rect x="0" y="0"
            width="${total_width}" height="${total_width}"
            fill="pink"/>`;
        if (this.selected_piece){
            output += this.selected_piece.get_piece_svg(total_width);
        }
        return output;
    }

    get_board_svg(total_width){
        var output = `<rect
            x="0" y="0" width="${total_width}" height="${total_width}" fill="black"
        />`;
        var field_width = total_width/4;
        output += '<g id="board">';

        for (var x=0; x<this.positions.length; x++) {
            for (var y=0; y<this.positions[x].length; y++) {
                output += `<g transform="translate(${field_width * x}, ${field_width * y})">
                    ${this.get_field(x, y, field_width, (x+y) % 2)}
                    ${(this.positions[x][y])?this.positions[x][y].get_piece_svg(field_width):''}
                </g>`;
            }
        }
        output += '</g>';
        return output;
    }

    get_field(x, y, field_width, alt_color) {
        var margin = field_width/20;
        var color = 'brown';
        if (alt_color) {
            color = 'purple';
        }
        return `
            <rect
                class="position"
                x_value="${x}"
                y_value="${y}"
                x="${margin}"
                y="${margin}"
                width="${field_width - margin*2}"
                height="${field_width - margin*2}"
                fill="${color}"
            />`;
    }
}
