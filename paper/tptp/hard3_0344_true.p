% hard3_0344  eq1=3273 eq2=4312  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(Y,f(X,f(Y,Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(X,Y)) = f(Z,f(W,W)) )).
