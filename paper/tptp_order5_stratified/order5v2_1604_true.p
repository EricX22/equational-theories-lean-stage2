% order5v2_1604  eq1=29934 eq2=30343  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(Z,f(Y,Y)))),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(X,f(f(X,Y),X))),Z) )).
