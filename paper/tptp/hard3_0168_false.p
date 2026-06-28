% hard3_0168  eq1=1506 eq2=359  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,X),f(Z,f(Z,X))) )).
fof(neg, negated_conjecture, ? [X] : ( f(X,X) != f(f(X,X),X) )).
