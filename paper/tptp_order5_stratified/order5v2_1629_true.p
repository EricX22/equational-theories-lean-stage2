% order5v2_1629  eq1=22625 eq2=54927  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,f(Y,X)),f(f(Z,W),U)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(Y,X)) = f(Y,f(f(X,Y),X)) )).
