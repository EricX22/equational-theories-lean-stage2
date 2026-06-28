% hard3_0128  eq1=1032 eq2=2076  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(X,f(Y,Z)),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,Y),Z),f(Y,Z)) )).
