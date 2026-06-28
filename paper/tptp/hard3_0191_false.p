% hard3_0191  eq1=1687 eq2=3312  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,X),f(f(X,Z),X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(X,f(Z,Y))) )).
