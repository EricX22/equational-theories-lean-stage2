% hard3_0355  eq1=3360 eq2=3505  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(Y,f(Y,f(Z,Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(f(Z,W),Z)) )).
