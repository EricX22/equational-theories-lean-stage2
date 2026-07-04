% order5_0241  eq1=42290 eq2=54172  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,V,W,X,Y,Z] : ( f(X,Y) = f(Z,f(W,f(X,f(U,V)))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(Y,Y)) != f(X,f(Y,f(X,Y))) )).
