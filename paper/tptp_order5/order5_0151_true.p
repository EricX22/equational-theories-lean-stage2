% order5_0151  eq1=7733 eq2=57907  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Y,f(f(Y,f(Y,Z)),X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(f(Y,X),Z),Z) )).
