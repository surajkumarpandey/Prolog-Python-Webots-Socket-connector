:- use_module(library(socket)).
:- use_module(library(streampool)).

create_client :-                        
        setup_call_catcher_cleanup(tcp_socket(Socket),
                                   tcp_connect(Socket, localhost:9999),
                                   exception(Ex),
                                   tcp_close_socket(Socket)),
	setup_call_cleanup(tcp_open_socket(Socket, In, Out),
                           chat_to_server(In, Out),
                           close_connection(In, Out)).
	


chat_to_server(In, Out) :-                          
	read_string(In, "]", "", End,X),        
	split_string(X, ",", "", List),
	nth0(0, List, Ps0),
        nth0(7, List, Ps7),
	number_string(P0, Ps0),
	number_string(P7, Ps7),	
	writeln(P0),writeln(P7),
	((P0 > 80 ; P7 > 80) ->
		reply(Out,l), writeln("left turn");
		reply(Out,f),writeln("Straight")),
	chat_to_server(In, Out).

chat_to_server(_In, _Out) :-
        print_message(warning,'chat failed'),!.

reply(Out,Direction):-
	format(Out,'~q',Direction),                  
        flush_output(Out).
	

    
close_connection(In, Out) :-
        close(In, [force(true)]),
        close(Out, [force(true)]).
