% hard3_0242  eq1=2164 eq2=2044  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),X),f(X,W)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(X,X),Y),f(Y,Y)) )).
