% order5_0083  eq1=7618 eq2=12698  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(X,f(f(Z,f(X,W)),W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Y,f(Z,X))),Y)) )).
