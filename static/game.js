$(document).ready(function () {
    namespace = '';
    let socket = io(namespace);
    socket.emit("disconnect from room")
    let username = "";
    let class_ = "";

    if (window.chrome) {
        $('#canvas').addClass("chrome_canvas");
    } else {
        $('#canvas').addClass("firefox_canvas");
    }

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

    if (window.location.pathname.includes("lobby")) {
        lobbyID = window.location.pathname.split("/").pop();
        $("#lobby_id").val(lobbyID).click(function () {$(this).unbind("click").select()});
    }
    if (window.location.hash.includes("lobby")) {
        lobbyID = window.location.hash.split("/").pop();
        $("#lobby_id").val(lobbyID).click(function () {$(this).unbind("click").select()});
    }

    fetch("/static_info").then(data => { return data.json() }).then(function (data) {
        $("#username").val(data.random_name)
        data.classes.forEach(function (val) {
        $("#class").append('<option value="' + val + '">' + val + '</option>')
    })
    })

     $("#class")
        .mouseover(function () {
            $("#menu_status_bar").text("вы можете выбрать один из классов: рыцарь, лучник, волшебник");
        })
        .mouseout(function () {
            $("#menu_status_bar").empty();
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
            $("#menu_status_bar").text("вставьте ID комнаты вашего друга");
        })
        .mouseout(function () {
            $("#menu_status_bar").empty();
        });
    socket.on('lobby players', function (msg) {
        $("#current_room_users").empty().append('<span><b>Игроки в текущей комнате:</b> </span>');

        msg.players.forEach(function (val) {
            $('#current_room_users').append('<span class="username">' + val.username + "</span>");
        })
    })
    socket.on("join success", function () {
         $('form#join :input').hide()
        $("#create_room_button").hide()
    })
    socket.on("error", function (msg) {
        switch (msg.errtype) {
            case "room_not_found": {
                $("#lobby_id").addClass("is-invalid")
                $("#lobby_id_form_error").empty().append(msg.message)
                break
            }
            case "duplicate_username": {
                $("#username").addClass("is-invalid")
                $("#username_form_error").empty().append(msg.message)
                break
            }
        }
        console.log(msg);
    })
    socket.on("lobby created", function (msg) {
        let url = window.location.protocol + "//" + window.location.host + "/lobby/" + msg.id
        $("#lobby_code").empty().append('Отправьте эту ссылку вашему другу чтобы поиграть вместе: <a id="join_link" href="' + url + '">' + msg.id + "</a>")
        $("#join_link").mouseover(function () {
                $("#menu_status_bar").text("скопируйте это значение своему товарищу");
            })
            .mouseout(function () {
                $("#menu_status_bar").empty();
            });
        $("#username_form_error").empty()
        $("#lobby_id_form_error").empty()
        $("#lobby_id").val(msg.id);
        lobbyID = msg.id;
        $('#create_room_button').val("Начать игру").text("Начать игру").unbind("click").click(function (event) {
            socket.emit("start", {lobby_id: $("#lobby_id").val(), username: username});
            return false
        }).show();
        window.location.hash = "/lobby/" + msg.id
    })
    socket.on("game started", function (msg) {
        $("#username_form_error").empty()
        if (lobbyID === "") {
            lobbyID = $("#lobby_id").val()
        }
        $("#game_field").css('display', 'flex');
        $("#game_over").hide();
        $("#menu").hide()
        $("#log").empty();
        // обработка кнопок управления
        $(document).keydown(function (event) {
            event.preventDefault();
            let action = undefined;
            switch (event.key) {
                case "w":
                case "ц":
                case 'ArrowUp': {
                    action = "up";
                    break
                }
                case "s":
                case "ы":
                case 'ArrowDown': {
                    action = "down";
                    break
                }
                case "a":
                case "ф":
                case 'ArrowLeft': {
                    action = "left";
                    break
                }
                case "d":
                case "в":
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
                if (val === username) {
                    $('#users').append('<span class="username active_user user_me">' + val + "</span>");
                } else {
                    $('#users').append('<span class="username active_user">' + val + "</span>");
                }

            } else {
                if (val === username) {
                    $('#users').append('<span class="username user_me">' + val + "</span>");
                } else {
                    $('#users').append('<span class="username">' + val + "</span>");
                }
            }
        })
        msg.dead_players.forEach(function (val) {
            if (val === username) {
                $('#users').append('<span class="username dead_user user_me">' + val + "</span>");
            } else {
                $('#users').append('<span class="username dead_user">' + val + "</span>");
            }

        })
        let plt = $("#canvas");
        plt.empty();
        plt.append(msg.visual);
        plt.append('<p>' + msg.stats_visual.join("<br>") + '</p>')
        $(".map_tile")
            .mouseover(function () {
                let tileId = $(this).attr('id');
                $("#tile_description").text(tileDescriptions[tileId]);
                $(this).css("outline", "solid yellow").css("outline-offset", "-3px")
            })
            .mouseout(function () {
                $("#tile_description").empty();
                $(this).css("outline", "")
            })
            .click(function () {
                $("#tile_description").empty();
                let cls = $(this).attr("id");
                if (!cls) {
                    return
                }
                let items = cls.split("_");
                let i = parseInt(items[items.length - 2]);
                let j = parseInt(items[items.length - 1]);
                socket.emit("move", {
                    username: username,
                    action: ["on_position_left", i, j],
                    lobby_id: lobbyID,
                })
            })
            .contextmenu(function () {
                $("#tile_description").empty();
                let cls = $(this).attr("id");
                if (!cls) {
                    return false
                }
                let items = cls.split("_")
                let i = parseInt(items[items.length - 2]);
                let j = parseInt(items[items.length - 1]);
                socket.emit("move", {
                    username: username,
                    action: ["on_position_right", i, j],
                    lobby_id: lobbyID,
                });
                return false;
            })

        let inventory = $("#inventory");
        inventory.empty();
        if (msg.inventory.length > 0) {
            inventory.append("<h4>Инвентарь</h4>");
        }
        msg.inventory.forEach(function (val, i) {
            let item_name = "inventory_item_" + i
            inventory.append('<li id="' + item_name + '" >' + val.name + ' (' + val.count + ')</li>')
            $("#" + item_name)
                .mouseover(function () {
                    $(this).css("background", "yellow")
                    $("#tile_description").append(val.description);
                })
                .mouseout(function () {
                    $(this).css("background", "none")
                    $("#tile_description").empty();
                })
                .click(function () {
                    $("#tile_description").empty();
                    socket.emit("move", {
                                username: username,
                                action: ["equip_or_use", val.name],
                                lobby_id: lobbyID
                    });
                    return false
                })
                .contextmenu(function () {
                    $("#tile_description").empty();
                    socket.emit("move", {
                                username: username,
                                action: ["drop_on_world", val.name],
                                lobby_id: lobbyID
                    });
                    return false
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
    })
    $("form#join").submit(function() { return false; });
    $('#connect_room_button').click(function (event) {
        $("#username").removeClass("is-invalid")
        $("#lobby_id").removeClass("is-invalid")
        username = $("#username").val()
        class_ = $("#class").val()
        lobbyID = $('#lobby_id').val()
        if (username === "" || class_ === "") {
            // TODO - say "you need to specify username and class beforehand" here
            return false
        }
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
        if (username === "") {
            $("#username").addClass("is-invalid");
            $("#username_form_error").empty().append("имя не должно быть пустым");
            return false
        }

        socket.emit('new room', {username: username, class: class_});
        return false;
    });
    $("#play_again_button").click(function () {
        console.log("restarting game");
        socket.emit("start", {lobby_id: lobbyID, username: username});
        return false
    })
});
