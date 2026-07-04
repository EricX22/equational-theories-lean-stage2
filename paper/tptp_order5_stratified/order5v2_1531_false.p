% order5v2_1531  eq1=24670 eq2=13027  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Z),Z),f(f(Y,Y),Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Y,f(Z,f(X,Z))),W)) )).
