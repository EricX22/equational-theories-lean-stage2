% hard3_0093  eq1=714 eq2=1075  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(Y,f(f(Y,X),Y))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(Y,f(f(X,f(X,Y)),X)) )).
