% hard3_0091  eq1=707 eq2=1996  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,f(Y,f(f(X,Y),Y))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(Z,Z)),f(Y,X)) )).
