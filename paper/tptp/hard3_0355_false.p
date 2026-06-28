% hard3_0355  eq1=3360 eq2=3505  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(Y,f(Y,f(Z,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,X) != f(Y,f(f(Z,W),Z)) )).
