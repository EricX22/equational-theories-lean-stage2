% hard3_0111  eq1=897 eq2=3467  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(X,Z),f(Z,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(X,f(f(Y,Z),X)) )).
