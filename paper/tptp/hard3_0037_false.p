% hard3_0037  eq1=205 eq2=3464  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(X,f(X,Y)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(X,f(f(Y,Y),X)) )).
