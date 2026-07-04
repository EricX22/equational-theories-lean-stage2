% order5v2_0641  eq1=13266 eq2=29395  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Z,f(Z,f(Y,X))),Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(Y,f(Z,f(Y,X)))),Y) )).
