:- use_module(library(socket)).
:- use_module(library(streampool)).

move(Host, Port,Message) :-                                 %% create a Prolog client. Send request to server (Host:Port) along with 'Message' to server. This sends motion commands to the Webots Robot
        setup_call_catcher_cleanup(tcp_socket(Socket),
                                   tcp_connect(Socket, Host:Port),
                                   exception(_),
                                   tcp_close_socket(Socket)),
        setup_call_cleanup(tcp_open_socket(Socket, In, Out),
                           chat_to_server(In, Out,Message),
                           close_connection(In, Out)).

chat_to_server(In, Out,Message) :-                          
        Term = Message,                                     %% Assign +Message to term variable
        (Term = end_of_file                                 %% If term = end_of_file then return
                -> true;
                format(Out,'~q',[Term]),                    %% if message is not null then write to +Out stream the +term 
                flush_output(Out),
                read_string(In,L,X),                        %% read the data of Input stream in X. This is the sensor data sent by the Webots server          
                writeln(X)
        ),!.

chat_to_server(_In, _Out,_Message) :-
        print_message(warning,'chat failed'),!.

    
close_connection(In, Out) :-
        close(In, [force(true)]),
        close(Out, [force(true)]).
       
