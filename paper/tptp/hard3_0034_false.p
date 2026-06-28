% hard3_0034  eq1=176 eq2=1096  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(Y,Y),f(X,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(X,f(Z,Y)),X)) )).
