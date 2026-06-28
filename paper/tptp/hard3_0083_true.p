% hard3_0083  eq1=626 eq2=3744  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(X,f(f(Y,Z),Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(X,Z),f(W,Y)) )).
