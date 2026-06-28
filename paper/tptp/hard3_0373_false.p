% hard3_0373  eq1=3730 eq2=3265  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(X,Y),f(Z,W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(X,f(Y,f(Z,Y))) )).
