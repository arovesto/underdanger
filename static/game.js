$(document).ready(function () {
    namespace = '';
    let socket = io(namespace);
    socket.emit("disconnect from room")
    let username = "";
    let class_ = "";
    let lobbyStarter = false;

    $( window ).unload(function() {
        console.log("disconnect unload")
        socket.emit("disconnect from room")
    })
    $( window ).bind('beforeunload', function() {
        console.log("disconnect beforeunload")
        socket.emit("disconnect from room")
    });
    let playerState = 'default';
    let lobbyID = "";

    fetch("/static_info").then(data => { return data.json() }).then(function (data) {
        $("#username").val(data.random_name)
        data.classes.forEach(function (val) {
        $("#class").append('<option value="' + val + '">' + val + '</option>')
    })
    })

     $("#class")
        .mouseover(function () {
            $("#tile_description").text("вы можете выбрать один из классов: рыцарь, лучник, волшебник");
        })
        .mouseout(function () {
            $("#tile_description").empty();
        });
     $("#username")
        .mouseover(function () {
            $("#tile_description").text("ваше имя в игре");
        })
        .mouseout(function () {
            $("#tile_description").empty();
        }).click(function () {
            $(this).unbind("click").select()
        });
    $("#lobby_id")
        .mouseover(function () {
            $("#tile_description").text("вставьте ID комнаты вашего друга");
        })
        .mouseout(function () {
            $("#tile_description").empty();
        });
    socket.on('lobby players', function (msg) {
        $("#users").empty()
        $("#sidebar_left").show()
        msg.players.forEach(function (val) {
            $('#users').append('<li>' + val.username + "</li>");
        })
    })
    socket.on("error", function (msg) {
        console.log(msg);
        // TODO log msg.message + msg.status here like "error happened"
    })
    socket.on("lobby created", function (msg) {
        let lobby = $("#lobby_id");
        lobby.val(msg.id);
        $('#create_room_button').val("Начать игру");
        lobby.mouseover(function () {
                $("#tile_description").text("скопируйте это значение своему товарищу");
            })
            .mouseout(function () {
                $("#tile_description").empty();
            });
        $('#create_room_button').unbind("click").click(function (event) {
            lobbyStarter = true;
            socket.emit("start", {lobby_id: $("#lobby_id").val(), username: username});
            return false
        })
    })
    socket.on("game started", function (msg) {
        if (lobbyID === "") {
            lobbyID = $("#lobby_id").val()
        }
        $("#game_field").css("background", "blanchedalmond");;
        $("#game_over").hide();
        $("#menu").empty()
        $("#log").empty();
        // обработка кнопок управления
        $(document).keydown(function (event) {
            event.preventDefault();
            let action = undefined;
            switch (event.key) {
                case 'ArrowUp': {
                    action = "up";
                    break
                }
                case 'ArrowDown': {
                    action = "down";
                    break
                }
                case 'ArrowLeft': {
                    action = "left";
                    break
                }
                case 'ArrowRight': {
                    action = "right";
                    break
                }
                case " ": {
                    action = "nothing";
                    break
                }
                case 'я':
                case 'z': {
                    if (playerState === 'attack') {
                        playerState = 'default';
                    } else {
                        playerState = 'attack';
                    }
                    break
                }
                case 'ч':
                case 'x': {
                    if (playerState === 'secondary_attack') {
                        playerState = 'default';
                    } else {
                        playerState = 'secondary_attack';
                    }
                    break
                }
                default: {
                    break
                }
            }
            if (action !== undefined) {
                if (action === 'nothing') {
                    socket.emit("move", {
                        username: username,
                        action: ["nothing"],
                        lobby_id: lobbyID
                    });
                    return
                }
                let action_type;
                switch (playerState) {
                    case 'attack': {
                        action_type = 'use_main_weapon'
                        break
                    }
                    case 'secondary_attack': {
                        action_type = "use_second_weapon"
                        break
                    }
                    case 'default': {
                        action_type = "move_player"
                        break
                    }
                }
                playerState = 'default';
                console.log(action_type, action)
                socket.emit("move", {
                    username: username,
                    action: [action_type, action],
                    lobby_id: lobbyID
                });
            }
        });

        console.log("game started!");
        // TODO - close everything before and go to game screen mode
    })
    socket.on("game over", function (msg) {
        $("#tile_description").empty();

        $(document).unbind('keydown');
        if (lobbyStarter) {
            $("#play_again_button").show()
        }

        if (msg.game_status === 'win') {
            $("#game_over_text").text('Вы нашли выход из подземелья!');
        } else {
            $("#game_over_text").text('Все погибли..., игра окончена.');
        }
        $("#game_over").show();

    })

    socket.on("update", function (msg) {
        $("#tile_description").empty();
        let tileDescriptions = msg.tile_descriptions;
        $("#users").empty();
        msg.players_names.forEach(function (val) {
            if (val === msg.active_player_name) {
                $('#users').append('<p style="background: cornflowerblue">' + val + "</p>");
            } else {
                $('#users').append('<p>' + val + "</p>");
            }
        })
        msg.dead_players.forEach(function (val) {
            $('#users').append('<p style="background: darkgray">' + val + "</p>");
        })
        let plt = $("#plot");
        plt.empty();
        plt.append('<p style="font-family:\'Consolas\', monospace;white-space: pre-wrap">' + msg.visual + '</p>');

        let inventory = $("#inventory");
        inventory.empty();
        if (msg.inventory.length > 0) {
            inventory.append("<h4>Инвентарь</h4>");
        }
        msg.inventory.forEach(function (val, i) {
            let item_name = "inventory_item_" + i
            inventory.append('<li id="' + item_name + '">' + val.name + ' (' + val.count + ')</li>')
            $("#" + item_name)
                .mouseover(function () {
                    $(this).css("background", "yellow")
                    $("#tile_description").append(val.description);
                })
                .mouseout(function () {
                    $(this).css("background", "none")
                    $("#tile_description").empty();
                })
                .click(function (event) {
                    $("#tile_description").empty();
                    socket.emit("move", {
                        username: username,
                        action: ["equip_or_use", val.name],
                        lobby_id: lobbyID
                    });
                });
        });
        let equipment = $("#equipment");
        equipment.empty();
        if (msg.equipment.length > 0) {
            equipment.append("<h4>Надето на героя</h4>");
        }
        msg.equipment.forEach(function (val, i) {
            let item_name = "equipment_item_" + i
            if (val.info !== null) {
                equipment.append('<li id="' + item_name + '">' + val.part + ": " + val.info.name + '</li>')
                $("#" + item_name)
                    .mouseover(function () {
                        $(this).css("background", "yellow")
                        $("#tile_description").append(val.info.description);
                    })
                    .mouseout(function () {
                        $(this).css("background", "none")
                        $("#tile_description").empty();
                    })
                    .click(function (event) {
                        $("#tile_description").empty();
                        socket.emit("move", {
                            username: username,
                            action: ["unequip", val.info.name],
                            lobby_id: lobbyID
                        });
                    });
            }
        })
        let magicBook = $("#magic_book");
        magicBook.empty();
        if (msg.magicbook.length > 0) {
            magicBook.append("<h4>Магическая книга</h4>");
        }
        msg.magicbook.forEach(function (val, i) {
            let item_name = "magic_item_" + i;
            magicBook.append('<li id="' + item_name + '">' + val.name + '</li>');
            $("#" + item_name)
                .mouseover(function () {
                    $(this).css("background", "yellow")
                    $("#tile_description").append(val.description);
                })
                .mouseout(function () {
                    $(this).css("background", "none")
                    $("#tile_description").empty();
                })
                .click(function (event) {
                    $("#tile_description").empty();
                    socket.emit("move", {
                        username: username,
                        action: ["magic", val.name],
                        lobby_id: lobbyID
                    });
                });
        })
        let tradeOffers = $("#trade_offers");
        tradeOffers.empty();
        if (msg.trade_offers !== null) {
            tradeOffers.append('<h4>Продавец ' + msg.trade_offers.trader_name + ' предлагает:</h4>')
            msg.trade_offers.trades.forEach(function (val, i) {
                let item_name = "trade_item_" + i
                tradeOffers.append('<li id="' + item_name + '">' + val.name + ' за ' + val.price + '</li>')
                $("#" + item_name)
                    .mouseover(function () {
                        $(this).css("background", "yellow")
                        $("#tile_description").append(val.description);
                    })
                    .mouseout(function () {
                        $(this).css("background", "none")
                        $("#tile_description").empty();
                    })
                    .click(function (event) {
                        $("#tile_description").empty();
                        socket.emit("move", {
                            username: username,
                            action: ["trade", val.name, msg.trade_offers.trader_name],
                            lobby_id: lobbyID
                        });
                    });
            })
        }
        let log = $("#log");
        log.append('<p>' + msg.log + '</p>').scrollTop(log[0].scrollHeight);

        plt.append('<p style="white-space: pre-wrap">' + msg.stats_visual.join("<br>") + '</p>')
        $(".map_tile")
            .mouseover(function () {
                let tileId = $(this).attr('id');
                $("#tile_description").text(tileDescriptions[tileId]);
            })
            .mouseout(function () {
                $("#tile_description").empty();
            });
    })
    $("form#join").submit(function() { return false; });
    $('#connect_room_button').click(function (event) {
        username = $("#username").val()
        class_ = $("#class").val()
        lobbyID = $('#lobby_id').val()
        if (username === "" || class_ === "" || lobbyID === "") {
            // TODO - say "you need to specify username and class beforehand" here
            return false
        }
        $('form#join :input').prop("disabled", true)
        socket.emit('join', {
            username: username,
            class: class_,
            lobby_id: lobbyID,
        });
        return false;
    });
    $('#create_room_button').click(function (event) {
        username = $("#username").val()
        class_ = $("#class").val()
        if (username === "" || class_ === "") {
            // TODO - say "you need to specify username and class beforehand" here
            return false
        }
        $('form#join :input').prop("disabled", true)
        $("#create_room_button").prop("disabled", false)
        socket.emit('new room', {username: username, class: class_});
        return false;
    });
    $("#play_again_button").click(function () {
        if (lobbyStarter) {
            console.log("restarting game")
            socket.emit("start", {lobby_id: lobbyID, username: username});
        } else {
            console.log("non lobby strater pressed play again button")
        }
    })
});
