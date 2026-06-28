% hard3_0259  eq1=2464 eq2=2273  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(f(Y,X),Z)),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(Y,f(Z,X))),X) )).
