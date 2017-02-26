game = null;

var create_game = function(player_name){
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
            window.location.hash = data.game_uuid;
            get_game(data.game_uuid);
        }
    });
};

var join_game = function(game_uuid, player_name){
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
            get_game(game_uuid);
        }
    });
};

var picking_move = function(game_uuid, player_name, number){
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
            get_game(game_uuid);
        }
    });
};
var placement_move = function(game_uuid, player_name, x, y){
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
            get_game(game_uuid);
        }
    });
};

var get_game = function(game_uuid){
    var request = $.ajax({
        url: `/api/v1/game/quarto/${game_uuid}`,
        method: "GET"
    });
    request.done(function(data, status, response) {
        if (response.status == 200) {
            game = new Game(
                game_uuid,
                data.player_a,
                data.player_b,
                data.winner,
                data.events
            );
            $('#game-space').html(
                game.get_svg()
            );
        }
    });
};

$(document).ready(function(){
    $('#control').on('click', '#js-create', function() {
        var player_name = $('#player-name').val();
        if (player_name !== ''){
            create_game(player_name);
        }
    });

    $('#control').on('click', '#js-join', function() {
        var game_uuid = $('#game-uuid').val();
        var player_name = $('#player-name').val();
        if (player_name !== '' && game_uuid !== ''){
            join_game(game_uuid, player_name);
        }

    });
    $('#control').on('click', '#js-watch', function() {
        var game_uuid = $('#game-uuid').val();
        if (game_uuid !== ''){
            get_game(game_uuid);
        }
    });



    $('#game-space').on('click', '#remaining_pieces .piece', function(event) {
        var target_value = event.currentTarget.getAttribute('value');
        picking_move(
            game.uuid,
            $('#player-name').val(),
            target_value
        );
    });

    $('#game-space').on('click', '#board .position', function(event) {
        var target_x = event.currentTarget.getAttribute('x_value');
        var target_y = event.currentTarget.getAttribute('y_value');
        placement_move(
            game.uuid,
            $('#player-name').val(),
            target_x,
            target_y
        );
    });

    var game_uuid = window.location.hash.substr(1);
    if (game_uuid !== ''){
        get_game(game_uuid);
    }
});
