-- control.lua

function split(inputstr, sep)
    if sep == nil then
            sep = "%s"
    end
    local t={}
    for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
            table.insert(t, str)
    end
    return t
end

commands.add_command("write_test_d", "DiscordControl command", function(e)
    game.write_file("output.txt", e.parameter, false, e.player_index)
end)


commands.add_command("write_test_multipram_d", "DiscordControl command", function(e)
    local split_param = split(e.parameter)
    game.write_file("param1.txt", split_param[1], false, e.player_index)
    game.write_file("param2.txt", split_param[2], false, e.player_index)

end)