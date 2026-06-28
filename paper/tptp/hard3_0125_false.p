% hard3_0125  eq1=1014 eq2=2318  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(U,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(X,f(Z,Z))),X) )).
