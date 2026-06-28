% hard3_0052  eq1=348 eq2=3734  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(Z,f(Y,Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(X,Z),f(X,W)) )).
