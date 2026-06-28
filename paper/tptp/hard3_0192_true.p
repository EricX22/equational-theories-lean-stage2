% hard3_0192  eq1=1695 eq2=680  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(Y,X),f(f(Y,Y),Y)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(Y,f(X,f(f(Y,Y),Y))) )).
