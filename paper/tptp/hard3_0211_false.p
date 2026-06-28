% hard3_0211  eq1=1979 eq2=4351  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(Z,Y)),f(Y,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Y)) != f(Z,f(Y,Y)) )).
