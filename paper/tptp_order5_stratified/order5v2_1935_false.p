% order5v2_1935  eq1=40426 eq2=37013  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,f(Z,Y)),W),W),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(f(Y,Z),W),f(X,Z)),X) )).
