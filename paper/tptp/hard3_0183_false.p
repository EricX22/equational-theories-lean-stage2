% hard3_0183  eq1=1642 eq2=1432  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,X),f(f(Y,Z),Z)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,X),f(Y,f(X,Y))) )).
