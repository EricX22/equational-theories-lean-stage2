% hard3_0062  eq1=419 eq2=842  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(X,f(X,f(Y,f(Y,X)))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(f(Y,Y),f(X,X))) )).
