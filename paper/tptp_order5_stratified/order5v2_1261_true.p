% order5v2_1261  eq1=29252 eq2=32923  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(X,f(X,f(X,f(X,X)))),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(f(f(Y,Z),Z),Y)),X) )).
