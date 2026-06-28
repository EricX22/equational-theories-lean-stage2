% hard3_0398  eq1=4573 eq2=4343  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(W,W),Y) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(Y,Y)) = f(Y,f(X,X)) )).
