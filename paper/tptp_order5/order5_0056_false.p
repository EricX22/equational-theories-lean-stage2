% order5_0056  eq1=35744 eq2=24991  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(Y,f(Y,X)),f(X,X)),X) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(X,f(Y,f(Y,Z))),f(W,U)) )).
