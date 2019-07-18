-- control.lua
function split(inputStr, sep)
    if sep == nil then
        sep = "%s"
    end
    local t = {}
    for str in string.gmatch(inputStr, "([^" .. sep .. "]+)") do
        table.insert(t, str)
    end
    return t
end

function get_position(player, direction, distance)
    local x = player.position.x
    local y = player.position.y
    distance = tonumber(distance)
    if direction == "n" then
        y = y - distance
    elseif direction == "s" then
        y = y + distance
    elseif direction == "e" then
        x = x + distance
    elseif direction == "w" then
        x = x - distance
    end
    return { x = x, y = y }
end

script.on_init(function()
    apply_long_reach_settings()
end)

function apply_long_reach_settings()
    local reach = 1000
    game.forces["player"].character_build_distance_bonus = reach
    game.forces["player"].character_build_distance_bonus = reach
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

commands.add_command("get_research_d", DISCORD_HELP_MESSAGE, function(e)
    local s = ""
    for k, v in pairs(game.players[e.player_index].force.technologies) do
        s = s .. "\n" .. v.name
    end
    game.write_file("output.txt", s, false, e.player_index)
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
    local split_param = split(e.parameter)

    local status, errorMsg = pcall(place_item, e, split_param)
    if status == false then
        game.write_file("output.txt", "ERROR\n" .. errorMsg, false,
                e.player_index)
    end
end)

commands.add_command("pick_up_item_d", DISCORD_HELP_MESSAGE, function(e)
    local status, errorMsg = pcall(pick_up_item, e)
    if status == false then
        game.write_file("output.txt", "ERROR\n" .. errorMsg, false,
                e.player_index)
    end
end)

commands.add_command("place_row_d", DISCORD_HELP_MESSAGE, function(e)
    local split_param = split(e.parameter)
    local count = tonumber(split_param[5])
    local offset = tonumber(split_param[6])
    local status, errorMsg
    local event = e
    for i = 1, count do
        split_param[3] = split_param[3] + offset
        place_item(event, split_param)
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

function place_item(e, split_param)
    local item = split_param[1]
    local direction = split_param[2]
    local distance = split_param[3]
    local rotation = split_param[4]
    local player = game.players[e.player_index]
    if player.get_item_count(item) > 0 then
        local stack = player.cursor_stack
        stack.set_stack({ name = item, count = 1 })

        local place_position = get_position(player, direction, distance)

        local rotation_table = { ["n"] = defines.direction.south, ["s"] = defines.direction.north, ["e"] = defines.direction.west, ["w"] = defines.direction.east }

        if game.players[e.player_index].can_build_from_cursor {
            position = place_position
        } then
            game.players[e.player_index].build_from_cursor {
                position = place_position,
                direction = rotation_table[rotation]
            }
            player.remove_item({ name = item, count = 1 })
            game.write_file("output.txt", "Placed " .. item, false, e.player_index)
        else
            game.write_file("output.txt", "ERROR\nCannot place at this location. Something is in the way.")
        end
        player.clean_cursor()
    else
        game.write_file("output.txt", "ERROR\nItem not in inventory", false,
                e.player_index)
    end
end

function pick_up_item(e)
    local split_param = split(e.parameter)
    local direction = split_param[1]
    local distance = split_param[2]
    local player = game.players[e.player_index]
    local pick_up_position = get_position(player, direction, distance)
    local item = game.surfaces[1].find_entities_filtered {
        position = pick_up_position
    }[1]
    game.write_file("output.txt", "Picked up " .. item.name, false,
            e.player_index)
    player.mine_entity(item)
end

