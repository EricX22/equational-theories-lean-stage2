% hard3_0070  eq1=487 eq2=114  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(X,f(Z,f(Y,X)))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(Y,f(f(X,X),X)) )).
