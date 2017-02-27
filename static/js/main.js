class Control{
    constructor(game_uuid, game_container, control_container){
        this.game = null;
        this.game_uuid = game_uuid;
        this.player_name = '';
        this.game_container = game_container;
        this.control_container = control_container;
        //Self-executing func which takes 'this' as self
        setInterval(
            function() {
                 this.keep_game_upto_date();
            }.bind(this), 1000
        );

        if (this.game_uuid !== ''){
            this.get_game(this.game_uuid);
        }
        this.draw_control();
        this.attach_listeners();
    }
    create_game(player_name){
        var request = $.ajax({
            url: "/api/v1/game/quarto",
            method: "POST",
            dataType: "json",
            data: {
                'player_name': player_name
            }
        });
        request.done(function(data, status, response) {
            if (response.status == 200) {
                // should be somewhere else.
                window.location.hash = data.game_uuid;
                this.get_game(data.game_uuid);
            }
        }.bind(this));
    }
    join_game(game_uuid, player_name){
        var request = $.ajax({
            url: `/api/v1/game/quarto/${game_uuid}/join`,
            method: "POST",
            dataType: "json",
            data: {
                'player_name': player_name
            }
        });
        request.done(function(data, status, response) {
            if (response.status == 200) {
                this.get_game(game_uuid);
            }
        }.bind(this));
    }
    picking_move(game_uuid, player_name, number){
        var request = $.ajax({
            url: `/api/v1/game/quarto/${game_uuid}/pick`,
            method: "POST",
            dataType: "json",
            data: {
                'player_name': player_name,
                'number': number,
            }
        });
        request.done(function(data, status, response) {
            if (response.status == 200) {
                this.get_game(game_uuid);
            }
        }.bind(this));
    }
    placement_move(game_uuid, player_name, x, y){
        var request = $.ajax({
            url: `/api/v1/game/quarto/${game_uuid}/place`,
            method: "POST",
            dataType: "json",
            data: {
                'player_name': player_name,
                'x': x,
                'y': y
            }
        });
        request.done(function(data, status, response) {
            if (response.status == 200) {
                this.get_game(game_uuid);
            }
        }.bind(this));
    }
    get_game(game_uuid){
        var request = $.ajax({
            url: `/api/v1/game/quarto/${game_uuid}`,
            method: "GET"
        });
        request.done(function(data, status, response) {
            if (response.status == 200) {
                this.game = new Game(
                    game_uuid,
                    data.player_a,
                    data.player_b,
                    data.winner,
                    data.events
                );
                $(this.game_container).html(
                    this.game.get_svg()
                );

            }
        }.bind(this));
    }
    keep_game_upto_date(){
        if (this.game && !this.game.winner) {
            this.get_game(this.game.uuid);
        }
    }
    draw_buttons(){
        var create_class = 'btn-warning';
        var join_class = 'btn-warning';
        var watch_class = 'btn-warning';
        if (this.player_name !== '' && this.game_uuid !== '') {
            join_class = 'btn-primary';
        }
        if (this.player_name !== '') {
            create_class = 'btn-primary';
        }
        if (this.game_uuid !== '') {
            watch_class = 'btn-primary';
        }
        $('#control-buttons').html(
            `<div class="col-sm-2">
                <button class="btn btn-block ${create_class}" id="js-create" type="submit">Create Game</button>
            </div>
            <div class="col-sm-2">
                <button class="btn btn-block ${join_class}" id="js-join" type="submit">Join Game</button>
            </div>
            <div class="col-sm-2">
                <button class="btn btn-block ${watch_class}" id="js-watch" type="submit">Watch Game</button>
            </div>`
        );
    }
    draw_control(){
        $(this.control_container).html(
            `<div class="row" id="control-inputs">
                <div class="col-sm-12">
                    <div class="form-group">
                        <label for="player-name">Your Name:</label>
                        <input type="text" class="form-control" id="player-name" placeholder="Your Name" value="${this.player_name}">
                    </div>
                </div>
                <div class="col-sm-12">
                    <div class="form-group">
                        <label for="player-name">Game Id:</label>
                        <input type="text" class="form-control" id="game-uuid" placeholder="Game Id" value="${this.game_uuid}">
                    </div>
                </div>
            </div>
            <div class="row" id="control-buttons">
            </div>`
        );
        this.draw_buttons();
    }
    attach_listeners(){

        $(this.control_container).on('input', 'input', function(){
            this.player_name = $('#player-name').val();
            this.game_uuid = $('#game-uuid').val();
            console.log($('#game-uuid').val());
            this.draw_buttons();
        }.bind(this));

        $(this.control_container).on('click', '#js-create', function() {
            var player_name = $('#player-name').val();
            if (player_name !== ''){
                this.create_game(player_name);
            }
        }.bind(this));

        $(this.control_container).on('click', '#js-join', function() {
            var game_uuid = $('#game-uuid').val();
            var player_name = $('#player-name').val();
            if (player_name !== '' && game_uuid !== ''){
                this.join_game(game_uuid, player_name);
            }

        }.bind(this));
        $(this.control_container).on('click', '#js-watch', function() {
            var game_uuid = $('#game-uuid').val();
            if (game_uuid !== ''){
                this.get_game(game_uuid);
            }
        }.bind(this));

        $(this.game_container).on('click', '#remaining_pieces .piece', function(event) {
            var target_value = event.currentTarget.getAttribute('value');
            this.picking_move(
                this.game.uuid,
                $('#player-name').val(),
                target_value
            );
        }.bind(this));

        $(this.game_container).on('click', '#board .position', function(event) {
            var target_x = event.currentTarget.getAttribute('x_value');
            var target_y = event.currentTarget.getAttribute('y_value');
            this.placement_move(
                this.game.uuid,
                $('#player-name').val(),
                target_x,
                target_y
            );
        }.bind(this));
    }
}

$(document).ready(function(){
    var game_uuid = window.location.hash.substr(1);
    var control = new Control(
        game_uuid, '#game-space', '#control'
    );
    $(document).ajaxError(
        function(event, request, settings){
            if (request && request.responseJSON && request.responseJSON.message){
                $("#errors").html(
                    `<div class="alert alert-warning alert-dismissible" role="alert">
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        Error requesting page ${settings.url},  ${request.responseJSON.message}
                    </div>`
                );
            }
        }
    );




});
