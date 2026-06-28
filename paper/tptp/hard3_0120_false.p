% hard3_0120  eq1=977 eq2=1860  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Z,Z),f(X,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,f(Y,Y)),f(Y,X)) )).
