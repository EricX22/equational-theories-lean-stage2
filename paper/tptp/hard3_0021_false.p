% hard3_0021  eq1=100 eq2=845  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(X,f(f(X,X),Y)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(f(Y,Y),f(Y,X))) )).
