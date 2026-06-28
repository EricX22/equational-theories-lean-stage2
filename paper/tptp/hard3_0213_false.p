% hard3_0213  eq1=2004 eq2=3883  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,Z)),f(W,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(f(Y,f(X,Z)),X) )).
