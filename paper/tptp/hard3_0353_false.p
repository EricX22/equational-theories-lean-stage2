% hard3_0353  eq1=3349 eq2=4682  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(Y,f(X,f(Z,Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,Y),Z) != f(f(Y,W),Z) )).
