% build the longest possible hamilton cycle in a m*n rechtangle
% every cell is counted as a vertice

#const m = 5. %length of the rechtangle
#const n = 5. %height of the rechtangle
#const l = m*n. % maximal length of the snake

f(1..m,1..n).
% rectangle of size m*n

connected(M1,N1,M2,N2) :- M1=M2, |N1-N2|=1, f(M1,N1), f(M2,N2).
connected(M1,N1,M2,N2) :- N1=N2, |M1-M2|=1, f(M1,N1), f(M2,N2).
% two nodes are directly connected if they are in the same row and the  difference between columns is 1, or if they are in the same column and the difference between rows is 1.

{cycle(L,M,N) : f(M,N)}  1 :- L=1..l.
% hamilton cycle of length of maximal l and completely inside the rectangle.
% M,N are the position of the node in the rechtangle, L is the order of the node in the hamilton cycle.
% for each l, there is at most one vertice in the cycle.

{cycle(1,M,N) : f(M,N)} = 1.
% start point of the cycle, denoted as 1.

L1=L2 :- cycle(L1,M,N), cycle(L2,M,N).
% every vertice can exist at most once in the cycle

in(L) :- cycle(L,_,_).
:- L=1..l, not in(L), in(L+1).	
% if L >= 1, then every L+1 needs to have the predicessor

:- cycle(L,M1,N1), cycle(L+1,M2,N2), not connected(M1,N1,M2,N2).
% every two neighbor vertices in the cycle need to be connected

:- cycle(1,M1,N1), cycle(L,M2,N2), L=#max{P : cycle(P,M,N)}, not connected(M1,N1,M2,N2).
% the first node and last node of the cycle need to be connected (so that it is a cycle)

#maximize{1,L : in(L)}.
% maximize the length of the cycle

#show cycle/3.
