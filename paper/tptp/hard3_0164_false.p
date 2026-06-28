% hard3_0164  eq1=1484 eq2=2351  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,X),f(X,f(Z,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(Y,f(Z,Y))),X) )).
