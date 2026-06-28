% hard3_0246  eq1=2248 eq2=3259  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(X,f(Y,Y))),Z) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(X,f(Y,f(X,Y))) )).
