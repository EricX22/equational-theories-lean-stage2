% order5_0235  eq1=1576 eq2=25201  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(Y,f(Y,W))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(X,f(Z,W))),f(Y,Z)) )).
