% order5_0150  eq1=35154 eq2=52659  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(f(Y,W),Y)),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(f(Z,f(Y,Y)),Y),W) )).
