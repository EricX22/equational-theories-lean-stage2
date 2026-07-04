% order5_0080  eq1=15807 eq2=54547  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,f(Y,X)),Y),Z)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,f(Y,Z)) = f(W,f(X,f(X,U))) )).
