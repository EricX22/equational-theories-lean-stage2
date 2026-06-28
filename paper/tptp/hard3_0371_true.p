% hard3_0371  eq1=3705 eq2=4362  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(f(Y,Z),f(Z,W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(Y,f(X,Z)) )).
