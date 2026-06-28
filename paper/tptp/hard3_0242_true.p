% hard3_0242  eq1=2164 eq2=2044  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),X),f(X,W)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,X),Y),f(Y,Y)) )).
