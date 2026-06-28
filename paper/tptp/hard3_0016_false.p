% hard3_0016  eq1=62 eq2=3762  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(X,f(X,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(Y,Y),f(Y,Y)) )).
