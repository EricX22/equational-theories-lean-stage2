% hard3_0394  eq1=4527 eq2=3439  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(Y,Y),X) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,Y) = f(Z,f(W,f(Y,U))) )).
