% hard3_0083  eq1=626 eq2=3744  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(X,f(f(Y,Z),Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(X,Z),f(W,Y)) )).
