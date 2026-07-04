% order5v2_1408  eq1=10516 eq2=48399  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,X),f(f(W,X),W))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,Y) != f(f(Z,f(Z,W)),f(U,Y)) )).
