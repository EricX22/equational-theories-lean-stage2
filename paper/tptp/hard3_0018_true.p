% hard3_0018  eq1=72 eq2=554  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,f(Y,f(X,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(Z,f(Y,f(X,X)))) )).
