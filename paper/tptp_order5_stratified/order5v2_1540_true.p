% order5v2_1540  eq1=29180 eq2=25210  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),Z),f(W,W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(X,f(Z,W))),f(W,Y)) )).
