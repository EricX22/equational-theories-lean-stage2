% order5_0186  eq1=12701 eq2=53707  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Y,f(Z,Y))),X)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(f(f(Z,W),Y),W),X) )).
