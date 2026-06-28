% hard3_0345  eq1=3277 eq2=4314  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(X,f(Z,W))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(Y,X)) = f(X,f(Y,Y)) )).
