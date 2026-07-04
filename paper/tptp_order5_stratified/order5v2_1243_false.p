% order5v2_1243  eq1=19798 eq2=3544  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(X,Y),f(f(Z,f(W,W)),Z)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,Y) != f(X,f(f(Z,W),U)) )).
