% hard3_0161  eq1=1458 eq2=1862  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,Y),f(Y,f(Z,Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(Y,Y)),f(Y,Z)) )).
