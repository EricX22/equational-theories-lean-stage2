% hard3_0365  eq1=3536 eq2=326  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(Z,Z),X)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(X,f(Y,Y)) )).
