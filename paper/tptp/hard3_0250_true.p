% hard3_0250  eq1=2265 eq2=3337  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(Y,f(Y,X))),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(X,f(Z,f(W,X))) )).
