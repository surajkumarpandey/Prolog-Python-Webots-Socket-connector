:- use_module(library(socket)).
:- use_module(library(streampool)).

:-dynamic running/1.

epuck(X) :- thread_create(init(X,ID),ID,[]),assert(running(ID)).

listen_to_epuck(M) :- thread_get_message(M).

close_epuck(ID)	:- retract(running(ID)).

init(X,ID) :-                        
        setup_call_catcher_cleanup(tcp_socket(Socket),
                                   tcp_connect(Socket, localhost:X),
                                   exception(Ex),
                                   tcp_close_socket(Socket)),
	setup_call_cleanup(tcp_open_socket(Socket, In, Out),
                           chat_to_server(In, Out,ID),
                           close_connection(In, Out)).
	

		

chat_to_server(In, Out,ID) :-
	(running(ID) ->                          
	(read_string(In, "]", "", End,X),        
	split_string(X, ",", "", List),
	nth0(0, List, Ps0),
        nth0(7, List, Ps7),
	number_string(P0, Ps0),
	number_string(P7, Ps7),	
	%writeln(P0),writeln(P7),
	((P0 > 75 ; P7 > 75) ->
		reply(Out,l), thread_send_message(main,[P0,P7,'left'],[]);
		reply(Out,f),thread_send_message(main,[P0,P7,'forward'],[])),
	chat_to_server(In, Out,ID));
	writeln('closing connection...'),reply(Out,'s')).

chat_to_server(_In, _Out,ID) :-
        print_message(warning,'chat failed'),!.

reply(Out,Direction):-
	format(Out,'~q',Direction),                  
        flush_output(Out).
	

    
close_connection(In, Out) :-
        close(In, [force(true)]),
        close(Out, [force(true)]),
	writeln('connection closed').

