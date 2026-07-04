% order5_0034  eq1=36703 eq2=53526  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(f(Y,Y),Z),f(X,Z)),X) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(f(f(Z,Y),X),W),Z) )).
