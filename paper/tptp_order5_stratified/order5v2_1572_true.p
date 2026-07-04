% order5v2_1572  eq1=35722 eq2=1760  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,f(X,Z)),f(W,X)),U) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,Z),f(f(X,Y),Y)) )).
