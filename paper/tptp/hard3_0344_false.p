% hard3_0344  eq1=3273 eq2=4312  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(Y,f(X,f(Y,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(X,Y)) != f(Z,f(W,W)) )).
