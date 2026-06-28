% hard3_0178  eq1=1573 eq2=4445  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Z),f(Y,f(Y,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(Y,X)) != f(f(Y,Y),X) )).
