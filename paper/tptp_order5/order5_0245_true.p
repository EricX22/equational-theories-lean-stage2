% order5_0245  eq1=34261 eq2=57091  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(Y,f(Z,Z))),Y) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(Y,f(W,U)),X) )).
