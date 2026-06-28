% hard3_0001  eq1=5 eq2=625  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(X,f(f(Y,Z),X))) )).
