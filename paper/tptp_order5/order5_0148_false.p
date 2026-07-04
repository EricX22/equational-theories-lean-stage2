% order5_0148  eq1=31736 eq2=1868  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(Y,f(f(Z,Z),f(W,U))),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(Y,Z)),f(X,Y)) )).
