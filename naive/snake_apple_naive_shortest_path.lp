#const l = m*n.

cell(1..m, 1..n).

connected(M1,N1,M2,N2) :- M1=M2, |N1-N2|=1, cell(M1,N1), cell(M2,N2).
connected(M1,N1,M2,N2) :- N1=N2, |M1-M2|=1, cell(M1,N1), cell(M2,N2).

#external apple(M,N) : cell(M,N).
path(M,N,1) :- apple(M,N).

#program add_snake(r).
{snake(M,N,P) : cell(M,N)} = 1 :- P = 1..r-1.
{path(M,N,P) : cell(M,N)}1 :- P = 2..l.
% define the path so that the snake can get to the apple
% the head of the path will be the actual position of the apple, and the tail of the path is the actual position of the head of the snake
% the path will not cross the actual position of the body parts of the snake.

P1=P2 :- path(M,N,P1), path(M,N,P2).
% every cell of the path can exist at most once
:- path(M1,N1,P), path(M2,N2,P+1), not connected(M1,N1,M2,N2).
% every two neighboring cells of the path must be connected
in_path(P) :- path(_,_,P).

:- in_path(P+1), not in_path(P), P=1..l.
% every cell of the path (except the first cell) needs to have predicesor in the path.
length(L) :- L=#max{P : path(_,_,P)}.
:- length(L), snake(M,N,1), not path(M,N,L).
% the head of the snake must be the last cell of the path.
whole_path(M,N,P) :- path(M,N,P), P=1..l.
whole_path(M,N,Q+L-1) :- length(L), snake(M,N,Q), Q>1.
new_snake(M,N,P) :- whole_path(M,N,P), P=1..r.

:- path(M,N,P), snake(M,N,L), L>1.
% for every other body part of the snake, it cannot be a cell in path.

#minimize{1,P : in_path(P)}.
% minimize the length of the path.
