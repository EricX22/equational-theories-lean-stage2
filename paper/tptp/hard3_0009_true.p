% hard3_0009  eq1=48 eq2=2255  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(X,f(X,f(X,Y))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(Y,f(X,X))),Z) )).
