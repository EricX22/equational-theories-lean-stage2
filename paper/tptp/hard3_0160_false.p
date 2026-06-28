% hard3_0160  eq1=1433 eq2=4631  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,X),f(Y,f(X,Z))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(f(X,Y),X) != f(f(X,Z),X) )).
