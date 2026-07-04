% order5v2_0935  eq1=14693 eq2=23013  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(X,Z),f(W,U)),W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(Z,W)),f(f(Y,W),Y)) )).
