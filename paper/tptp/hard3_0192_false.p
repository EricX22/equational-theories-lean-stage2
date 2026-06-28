% hard3_0192  eq1=1695 eq2=680  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(Y,X),f(f(Y,Y),Y)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(Y,f(X,f(f(Y,Y),Y))) )).
