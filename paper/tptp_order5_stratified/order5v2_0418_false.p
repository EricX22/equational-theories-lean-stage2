% order5v2_0418  eq1=31525 eq2=14613  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,X),f(X,W))),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(f(X,Y),f(Z,Z)),W)) )).
