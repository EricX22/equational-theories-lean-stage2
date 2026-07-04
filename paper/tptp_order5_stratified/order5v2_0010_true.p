% order5v2_0010  eq1=11076 eq2=57278  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(X,f(Y,X)),f(X,Z))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(W,f(U,X)),X) )).
