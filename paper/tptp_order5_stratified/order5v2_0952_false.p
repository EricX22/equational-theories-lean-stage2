% order5v2_0952  eq1=21636 eq2=22674  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(X,Z)),f(X,f(X,Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(Y,Z)),f(f(X,Z),W)) )).
