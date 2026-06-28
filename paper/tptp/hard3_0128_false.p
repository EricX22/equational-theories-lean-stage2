% hard3_0128  eq1=1032 eq2=2076  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(X,f(Y,Z)),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,Y),Z),f(Y,Z)) )).
