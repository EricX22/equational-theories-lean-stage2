% order5_0210  eq1=16027 eq2=56527  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(Z,f(W,Z)),U),X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(X,Y)) != f(f(Y,f(X,X)),X) )).
