% hard3_0190  eq1=1682 eq2=4515  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(Y,X),f(f(X,X),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Z)) != f(f(X,Z),Y) )).
