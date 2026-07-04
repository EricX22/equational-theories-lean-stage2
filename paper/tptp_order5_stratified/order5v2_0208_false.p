% order5v2_0208  eq1=37491 eq2=55368  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,f(X,f(Z,W))),W),U) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Z)) != f(Z,f(f(Y,Z),X)) )).
