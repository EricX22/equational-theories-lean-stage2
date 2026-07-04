% order5v2_1077  eq1=1600 eq2=57806  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(Z,f(W,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,Y)) != f(f(f(Z,W),Z),Z) )).
