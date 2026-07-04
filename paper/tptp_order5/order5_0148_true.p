% order5_0148  eq1=31736 eq2=1868  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,f(f(Z,Z),f(W,U))),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(Y,Z)),f(X,Y)) )).
