#const m = 7. %height of the rechtangle
#const n = 8. %length of the rechtangle
#const l = 15. %length of the snake

f(1..m,1..n).
% rectangle of size m*n

{trace(L,M,N) : f(M,N)} = 1 :- L=1..l.
% trace of length 4 and completely inside the rectangle
% for each l, there is only one trace

:- trace(L1,M,N), trace(L2,M,N), L1!=L2.
% no two points of the trace can be in the same cell

:- trace(L,M,N), trace(L + 1,M1,N1), M1!=M, N1!=N.
% two continulious points of the trace cannot be in the different columns and rows at the same time

:- trace(L,M1,N), trace(L + 1,M2,N), |M1 - M2| != 1.
% two continulious points of the trace if have the same row, then the columns must be different by 1

:- trace(L,M,N1), trace(L + 1,M,N2), |N1 - N2| != 1.

#minimize{|M1-M2| + |N1-N2| : trace(1,M1,N1), trace(l,M2,N2)} .

#show trace/3.
