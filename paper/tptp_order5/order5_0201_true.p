% order5_0201  eq1=19818 eq2=25062  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(Y,X),f(f(X,f(Y,X)),Y)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(X,f(Y,f(Z,W))),f(W,U)) )).
