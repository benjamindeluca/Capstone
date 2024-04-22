%% Creating Client Instance:
clc
clear 
tcpipClient = tcpclient('127.0.0.1',5000, "Timeout", 1)

% Initial String testing just x, y, z
jsonStr = '{"object_name": "Box", "location": {"x": 5.6, "y": 0, "z":10.0}}\r';


jsonStr = ['{"object_name": "Sphere",' ...
                '"transform": {' ...
                    '"position": {"x": 1, "y": 1, "z": 0}' ...
                             '}' ...
           '}'];

fprintf("Sending JSON String: %s\n", jsonStr);

write(tcpipClient, jsonStr)
read(tcpipClient)
% Wait for confirmation that the message has been sent
flush(tcpipClient)
fprintf("Flush Complete")
delete(tcpipClient);