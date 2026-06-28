% hard3_0397  eq1=4573 eq2=4306  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(W,W),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(X,Y)) = f(Z,f(Y,W)) )).
