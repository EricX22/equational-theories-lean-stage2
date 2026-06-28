% hard3_0073  eq1=541 eq2=1366  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Z,f(X,f(Y,X)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,Y),X),X)) )).
