% order5_0075  eq1=34233 eq2=36740  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(Y,f(X,W))),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Y),Z),f(Z,Z)),W) )).
