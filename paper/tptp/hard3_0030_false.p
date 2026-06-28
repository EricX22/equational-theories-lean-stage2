% hard3_0030  eq1=155 eq2=3509  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,X),f(Y,Z)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(X,f(f(X,X),Y)) )).
