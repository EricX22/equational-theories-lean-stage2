% order5_0240  eq1=56944 eq2=54460  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(X,f(X,X)),Y) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,f(Y,Z)) = f(Y,f(W,f(U,X))) )).
