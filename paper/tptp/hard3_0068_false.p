% hard3_0068  eq1=456 eq2=1051  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(Y,f(Z,f(Z,Z)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(X,f(f(Y,f(Y,Z)),X)) )).
