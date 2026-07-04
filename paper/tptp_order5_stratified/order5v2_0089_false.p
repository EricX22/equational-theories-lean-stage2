% order5v2_0089  eq1=30881 eq2=48437  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(f(W,X),W))),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(Z,f(W,Y)),f(Y,Z)) )).
