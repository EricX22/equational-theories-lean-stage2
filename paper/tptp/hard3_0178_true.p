% hard3_0178  eq1=1573 eq2=4445  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),f(Y,f(Y,X))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(Y,X)) = f(f(Y,Y),X) )).
