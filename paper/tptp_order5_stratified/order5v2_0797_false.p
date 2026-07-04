% order5v2_0797  eq1=15896 eq2=44532  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,f(Z,Y)),X),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(Y,f(f(X,f(Y,Z)),Z)) )).
