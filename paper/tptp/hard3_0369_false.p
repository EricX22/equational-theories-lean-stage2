% hard3_0369  eq1=3676 eq2=4682  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(f(Y,X),f(X,Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,Y),Z) != f(f(Y,W),Z) )).
