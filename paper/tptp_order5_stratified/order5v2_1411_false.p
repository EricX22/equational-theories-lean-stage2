% order5v2_1411  eq1=1549 eq2=55527  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(Z,f(W,Z))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,f(Y,Z)) != f(W,f(f(U,X),W)) )).
