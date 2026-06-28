% hard3_0194  eq1=1709 eq2=1941  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,X),f(f(Z,Z),X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(Y,Z)),f(X,X)) )).
