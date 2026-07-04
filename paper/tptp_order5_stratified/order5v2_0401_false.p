% order5v2_0401  eq1=21992 eq2=7845  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,Y)),f(W,f(X,Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Z,f(f(X,f(X,W)),Z))) )).
