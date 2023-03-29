#const l = m*n.
%number of cells, or maximal length of the hamilitonion cycle

cell(1..m, 1..n).
%every cell in the rechtangle is considered to be a node.

connected(M1,N1,M2,N2) :- M1=M2, |N1-N2|=1, cell(M1,N1), cell(M2,N2).
connected(M1,N1,M2,N2) :- N1=N2, |M1-M2|=1, cell(M1,N1), cell(M2,N2).
% two nodes are directly connected if they are in the same row and the  difference between columns is 1, 
% or if they are in the same column and the difference between rows is 1.

% now the job is to create all hamiltonian cycle
{cycle(M,N,T) : cell(M,N)} = 1 :- T = 1..l.
% create a hamiltonian cycle with a length of l inside the rechtangle
% cycle(M,N,T) means that the node (M,N) is the T-th node in the cycle

:- cycle(M,N,T1), cycle(M,N,T2), T1 != T2.
% constraint that no node can be visited twice

:- cycle(M1,N1,T), cycle(M2,N2,T+1), not connected(M1,N1,M2,N2).
% every two neighbouring nodes in the cycle must be connected

:- cycle(M1,N1,1), cycle(M2,N2,l), not connected(M1,N1,M2,N2).
% the first and the last node in the cycle must be connected

next(M1,N1,M2,N2) :- cycle(M1,N1,T), cycle(M2,N2,T+1).
next(M1,N1,M2,N2) :- cycle(M1,N1,l), cycle(M2,N2,1).
% create a new function next that is true if the two nodes are neighbouring in the cycle (the order is important)

#external apple(P,Q) : cell(P,Q).
new_snake(P,Q,1) :- apple(P,Q).
% technically, the apple is the head of the snake

#program add_snake(r).
{snake(M,N,r-1) : cell(M,N)} = 1.
% snake(M,N,P) means that the cell(M,N) is in the P-th body part of the snake.

% the snake is the input (the old snake before eating the apple)
:- snake(M1,N1,r-2), snake(M2,N2,r-1), cycle(M1,N1,T1), cycle(M2,N2,T2), not next(M1,N1,M2,N2).% every two neighbouring body parts of a snake also must be neighbours in the hamiltionian cycle
% here the snake also has the same direction as the hamiltonian cycle, so that the new snake also can remain the same direction

{new_snake(M,N,r) : cell(M,N)} = 1.
:- new_snake(M1,N1,P), new_snake(M2,N2,P+1), not connected(M1,N1,M2,N2).
% create the new snake
:- new_snake(M,N,1), not cycle(M,N,1).
% tail of the snake is also the tail of the hamiltonian cycle
:- new_snake(M,N,r), not cycle(M,N,r).
% every other body part of the snake is measured from the tail of the hamiltonian cycle.

#minimize{L : cycle(M,N,L), snake(M,N,1)}.
