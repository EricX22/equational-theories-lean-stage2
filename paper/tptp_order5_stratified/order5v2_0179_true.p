% order5v2_0179  eq1=22672 eq2=20265  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(Y,Z)),f(f(X,Z),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,Z),f(f(Z,f(X,X)),Z)) )).
