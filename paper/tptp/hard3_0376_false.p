% hard3_0376  eq1=3791 eq2=4283  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(f(Z,X),f(Y,Z)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(X,Y)) != f(X,f(Y,X)) )).
