% order5_0176  eq1=50869 eq2=43021  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(f(X,W),Z)),U) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,Y) != f(Z,f(Y,f(f(Y,W),U))) )).
