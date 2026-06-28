% hard3_0346  eq1=3277 eq2=4365  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(X,f(Z,W))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(Y,f(Z,W)) )).
