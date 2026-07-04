% order5_0151  eq1=7733 eq2=57907  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(Y,f(f(Y,f(Y,Z)),X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Z)) != f(f(f(Y,X),Z),Z) )).
