% order5v2_1625  eq1=13038 eq2=19908  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Y,f(Z,f(Y,Y))),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,X),f(f(Z,f(Y,Z)),Z)) )).
