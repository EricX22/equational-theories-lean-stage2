% hard3_0062  eq1=419 eq2=842  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(X,f(X,f(Y,f(Y,X)))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(f(Y,Y),f(X,X))) )).
