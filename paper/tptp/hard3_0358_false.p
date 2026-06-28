% hard3_0358  eq1=3476 eq2=4470  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(Y,f(f(X,Y),Z)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(Y,Y)) != f(f(X,X),Y) )).
