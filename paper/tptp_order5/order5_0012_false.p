% order5_0012  eq1=32605 eq2=46306  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,f(Z,W)),Z)),W) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(Y,Y),f(X,f(X,Y))) )).
