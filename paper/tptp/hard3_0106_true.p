% hard3_0106  eq1=853 eq2=160  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(Y,Z),f(X,Y))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,Y),f(Y,Y)) )).
