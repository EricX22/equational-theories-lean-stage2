% hard3_0172  eq1=1521 eq2=483  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Y),f(X,f(Z,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(X,f(Z,f(X,X)))) )).
