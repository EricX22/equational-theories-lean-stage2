% order5_0201  eq1=19818 eq2=25062  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(Y,X),f(f(X,f(Y,X)),Y)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(X,f(Y,f(Z,W))),f(W,U)) )).
