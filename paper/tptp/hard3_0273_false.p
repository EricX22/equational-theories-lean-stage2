% hard3_0273  eq1=2633 eq2=3670  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,W),W)),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(f(X,Y),f(Z,X)) )).
