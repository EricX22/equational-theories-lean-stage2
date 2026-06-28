% hard3_0308  eq1=2884 eq2=2045  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,f(Y,Z)),X),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,X),Y),f(Y,Z)) )).
