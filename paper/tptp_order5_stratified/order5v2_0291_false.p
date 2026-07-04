% order5v2_0291  eq1=25433 eq2=56421  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(X,W))),f(Z,Y)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,f(Y,Z)) != f(f(W,U),f(W,Z)) )).
