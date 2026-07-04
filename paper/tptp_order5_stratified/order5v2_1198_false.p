% order5v2_1198  eq1=10646 eq2=39824  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,Z),f(f(Y,W),Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(f(X,f(X,Y)),Z),W),Z) )).
