% hard3_0069  eq1=483 eq2=2087  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(X,f(Z,f(X,X)))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(Y,X),X),f(X,X)) )).
