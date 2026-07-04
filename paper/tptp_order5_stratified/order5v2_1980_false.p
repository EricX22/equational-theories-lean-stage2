% order5v2_1980  eq1=16431 eq2=54300  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(f(f(X,Z),W),Y),Z)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,f(Y,Y)) != f(Z,f(W,f(Z,U))) )).
