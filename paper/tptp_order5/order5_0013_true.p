% order5_0013  eq1=12723 eq2=38148  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Z,f(X,Z))),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,f(f(Y,Z),X)),X),Y) )).
