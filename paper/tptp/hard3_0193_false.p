% hard3_0193  eq1=1699 eq2=1075  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,X),f(f(Y,Z),Z)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(Y,f(f(X,f(X,Y)),X)) )).
