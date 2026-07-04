% order5_0056  eq1=35744 eq2=24991  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(Y,f(Y,X)),f(X,X)),X) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(X,f(Y,f(Y,Z))),f(W,U)) )).
