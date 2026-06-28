% hard3_0255  eq1=2393 eq2=4272  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(Y,W))),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(X,X)) = f(Y,f(X,X)) )).
