% order5_0215  eq1=25110 eq2=16437  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(Y,f(X,f(Y,X))),f(Y,Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(f(f(X,Z),W),Z),W)) )).
