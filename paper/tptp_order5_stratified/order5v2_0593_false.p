% order5v2_0593  eq1=26832 eq2=57288  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,X),f(X,X)),f(Z,W)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,f(Y,Z)) != f(f(W,f(U,Y)),U) )).
