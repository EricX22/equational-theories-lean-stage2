% order5_0068  eq1=53336 eq2=11574  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(f(f(Y,Y),Y),Y),Z) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(W,X)),f(X,U))) )).
