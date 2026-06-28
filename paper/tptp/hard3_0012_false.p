% hard3_0012  eq1=52 eq2=3664  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(X,f(Y,f(X,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(f(X,Y),f(X,X)) )).
