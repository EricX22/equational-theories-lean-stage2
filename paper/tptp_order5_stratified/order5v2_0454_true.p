% order5v2_0454  eq1=13877 eq2=4281  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Y,f(f(Y,Z),X)),Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(X,X)) = f(Y,f(Z,W)) )).
