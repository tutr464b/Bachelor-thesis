#const l = m*n.
%number of cells, or maximal length of the hamilitonion cycle


cell(1..m, 1..n).
%every cell in the rechtangle is considered to be a node.

connected(M1,N1,M2,N2) :- M1=M2, |N1-N2|=1, cell(M1,N1), cell(M2,N2).
connected(M1,N1,M2,N2) :- N1=N2, |M1-M2|=1, cell(M1,N1), cell(M2,N2).
% two nodes are directly connected if they are in the same row and the  difference between columns is 1, 
% or if they are in the same column and the difference between rows is 1.

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

cycle(1,1,1).
%fix the cycle by fixing the first node of the cycle.

#external apple(P,Q) : cell(P,Q).
new_snake(P,Q,1) :- apple(P,Q).

#program add_snake(r).
{new_snake(M,N,r) : cell(M,N)} = 1.
:- new_snake(M1,N1,R-1), cycle(M1,N1,T1), new_snake(M2,N2,R), cycle(M2,N2,T2), not next(M1,N1,M2,N2).
% after every iteration, add the tail to the snake, so that it is connected to the last tail of the snake and still follow the hamiiltonian cycle