% order5v2_1239  eq1=15549 eq2=16404  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(f(X,f(Z,W)),X),Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(f(f(X,Z),Y),W),Z)) )).
