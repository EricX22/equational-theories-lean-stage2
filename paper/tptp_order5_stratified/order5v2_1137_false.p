% order5v2_1137  eq1=33560 eq2=3847  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(f(Z,W),Z),Z)),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(Z,W),f(Z,Y)) )).
