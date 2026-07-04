% order5_0055  eq1=29304 eq2=55775  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(X,f(Y,f(X,f(X,X)))),Y) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(Y,X)) = f(f(X,Y),f(X,Y)) )).
