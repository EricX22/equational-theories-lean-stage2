% order5v2_1177  eq1=7776 eq2=47772  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(Y,f(f(Z,f(Y,Y)),Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(f(Y,f(Y,Y)),f(Y,Z)) )).
