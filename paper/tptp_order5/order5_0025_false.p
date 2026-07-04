% order5_0025  eq1=12281 eq2=50602  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(Z,X),W),f(Z,U))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(X,f(f(Z,Y),Z)),Y) )).
