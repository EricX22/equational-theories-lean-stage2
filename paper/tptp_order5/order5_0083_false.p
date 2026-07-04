% order5_0083  eq1=7618 eq2=12698  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(X,f(f(Z,f(X,W)),W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(X,f(f(Y,f(Y,f(Z,X))),Y)) )).
