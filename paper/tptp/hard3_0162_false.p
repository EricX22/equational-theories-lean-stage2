% hard3_0162  eq1=1462 eq2=4135  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,Y),f(Z,f(X,Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(f(X,Y),Z),Z) )).
