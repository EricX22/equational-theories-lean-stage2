% hard3_0280  eq1=2675 eq2=3312  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,Y),f(Y,Z)),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(X,f(Z,Y))) )).
