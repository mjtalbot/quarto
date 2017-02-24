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

var get_game = function(game_uuid){
    var request = $.ajax({
        url: `/api/v1/game/quarto/${game_uuid}`,
        method: "GET"
    });
    request.done(function(data, status, response) {
        if (response.status == 200) {
            game = new Game(
                game_uuid,
                data['player_a'],
                data['player_b'],
                data['events']
            );
            console.log(game)
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
});
