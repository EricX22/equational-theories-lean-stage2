% order5_0240  eq1=56944 eq2=54460  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(X,f(X,X)),Y) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,f(Y,Z)) != f(Y,f(W,f(U,X))) )).
