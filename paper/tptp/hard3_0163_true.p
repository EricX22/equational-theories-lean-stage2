% hard3_0163  eq1=1480 eq2=528  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,X),f(X,f(X,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(Y,f(Z,f(Z,X)))) )).
