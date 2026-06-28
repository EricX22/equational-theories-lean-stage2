% hard3_0106  eq1=853 eq2=160  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(Y,Z),f(X,Y))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,Y),f(Y,Y)) )).
