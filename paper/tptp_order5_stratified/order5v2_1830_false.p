% order5v2_1830  eq1=19991 eq2=38487  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(f(X,f(Z,W)),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,f(f(Y,Z),Z)),Y),X) )).
