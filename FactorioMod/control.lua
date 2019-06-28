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

commands.add_command("write_test_d", DISCORD_HELP_MESSAGE, function(e)
    game.write_file("output.txt", e.parameter, false, e.player_index)
end)

commands.add_command("write_test_multiparam_d", DISCORD_HELP_MESSAGE, function(e)
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
    else
        game.write_file("output.txt", "Started crafting: " .. split_param[2])
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
            game.write_file("output.txt", "Started researching: ".. e.parameter)
        end
    end
end)

function set_research(e)
    game.players[e.player_index].force.current_research = e.parameter
end
function craft_item(e)
    local split_param = split(e.parameter)
    local count = game.players[e.player_index].begin_crafting {
        count = split_param[1],
        recipe = split_param[2]
    }
end