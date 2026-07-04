% order5v2_0290  eq1=19090 eq2=53356  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(f(X,X),f(Z,W))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(f(f(Y,Y),Z),W),W) )).
