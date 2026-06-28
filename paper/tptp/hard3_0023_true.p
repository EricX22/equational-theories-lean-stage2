% hard3_0023  eq1=110 eq2=10  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(Y,Z),X)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(Y,X)) )).
