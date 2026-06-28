% hard3_0359  eq1=3483 eq2=3766  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(Y,f(f(Y,X),Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(Y,Y),f(Z,Z)) )).
