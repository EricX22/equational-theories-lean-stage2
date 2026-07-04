% order5_0199  eq1=61517 eq2=46503  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(f(X,Y),Z) = f(f(Z,f(Z,X)),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,Y),f(X,f(Y,W))) )).
