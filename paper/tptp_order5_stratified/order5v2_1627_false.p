% order5v2_1627  eq1=31357 eq2=49749  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(Y,f(f(X,Z),f(W,U))),U) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,Y) != f(f(X,f(Z,f(Z,W))),U) )).
