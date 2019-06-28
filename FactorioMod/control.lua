-- control.lua
function split(inputstr, sep)
    if sep == nil then sep = "%s" end
    local t = {}
    for str in string.gmatch(inputstr, "([^" .. sep .. "]+)") do
        table.insert(t, str)
    end
    return t
end

DISCORD_HELP_MESSAGE = "DiscordControl command. DO NOT USE MANUALLY "

commands.add_command("zoom_d", DISCORD_HELP_MESSAGE, function(e)
    if e.parameter == "" or e.parameter == nil then
        game.players[e.player_index].zoom = 0.75
    else
        game.players[e.player_index].zoom = e.parameter
    end
end)

commands.add_command("write_test_d", DISCORD_HELP_MESSAGE, function(e)
    game.write_file("output.txt", e.parameter, false, e.player_index)
end)

commands.add_command("write_test_multiparam_d", DISCORD_HELP_MESSAGE,
    function(e)
        local split_param = split(e.parameter)
        game.write_file("param1.txt", split_param[1], false, e.player_index)
        game.write_file("param2.txt", split_param[2], false, e.player_index)
    end)

commands.add_command("craft_item_d", DISCORD_HELP_MESSAGE, function(e)
    local split_param = split(e.parameter)
    local status, errorMsg = pcall(craft_item, e)
    if status == false then
        game.write_file("output.txt", "ERROR\n" .. errorMsg, false,
            e.player_index)
    end
end)

commands.add_command("set_research_d", DISCORD_HELP_MESSAGE, function(e)
    local isStop = false
    if e.parameter == "" or e.parameter == "stop" or e.parameter == nil then
        e.parameter = nil
        isStop = true
    end

    local status, errorMsg = pcall(set_research, e)

    if status == false then
        game.write_file("output.txt", "ERROR\n" .. errorMsg, false,
            e.player_index)
    else
        if isStop then
            game.write_file("output.txt", "Stopped current research.", false,
                e.player_index)
        else
            game.write_file("output.txt",
                "Started researching: " .. e.parameter, false,
                e.player_index)
        end
    end
end)

commands.add_command("place_item_d", DISCORD_HELP_MESSAGE, function(e)
    local status, errorMsg = pcall(place_item, e)
    if status == false then
        game.write_file("output.txt", "ERROR\n" .. errorMsg, false,
            e.player_index)
    end
end)

function set_research(e)
    game.players[e.player_index].force.current_research = e.parameter
end

function craft_item(e)
    local split_param = split(e.parameter)
    local count_crafted = game.players[e.player_index].begin_crafting {
        count = split_param[1],
        recipe = split_param[2]
    }
    game.write_file("output.txt", count_crafted, false, e.player_index)
end

function place_item(e)
    local split_param = split(e.parameter)
    local item = split_param[1]
    local direction = split_param[2]
    local distance = split_param[3]
    local rotation = split_param[4]
    local player = game.players[e.player_index]

    if player.get_item_count(item) > 0 then
        local stack = player.cursor_stack
        stack.set_stack({ name = item, count = 1 })

        local x = player.position.x
        local y = player.position.y
        if direction == "n" then
            y = y - distance
        elseif direction == "s" then
            y = y + distance
        elseif direction == "e" then
            x = x + distance
        elseif direction == "w" then
            x = x - distance
        end

        local place_position = { x, y }


        if rotation == "n" then
            local place_rotation = { defines.direction.north }
        elseif rotation == "s" then
            local place_rotation = { defines.direction.south }
        elseif rotation == "e" then
            local place_rotation = { defines.direction.east }
        elseif rotation == "w" then
            local place_rotation = { defines.direction.north }
        end

        game.players[e.player_index].build_from_cursor {
            position = place_position,
            direction = place_rotation
        }
        player.clean_cursor()
        player.remove_item({ name = item, count = 1 })
        game.write_file("output.txt",
            "Placed " .. item, false,
            e.player_index)
    else
        game.write_file("output.txt",
            "ERROR\nItem not in inventory", false,
            e.player_index)
    end
end