% order5v2_1031  eq1=25564 eq2=15609  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(Z,f(Z,Z))),f(Y,Y)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(Y,f(f(f(Y,f(X,Z)),W),U)) )).
