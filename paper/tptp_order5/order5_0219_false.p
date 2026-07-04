% order5_0219  eq1=44103 eq2=7332  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(W,W),f(Y,Y))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(X,f(f(X,f(Y,X)),Y))) )).
