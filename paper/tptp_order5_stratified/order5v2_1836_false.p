% order5v2_1836  eq1=34495 eq2=42623  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,f(U,W))),Y) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(X,f(X,f(f(Y,Y),Y))) )).
