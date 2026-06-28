% hard3_0113  eq1=916 eq2=1238  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(f(Y,Y),f(X,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(f(f(Y,X),X),X)) )).
