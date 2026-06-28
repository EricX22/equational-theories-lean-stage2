% hard3_0183  eq1=1642 eq2=1432  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,X),f(f(Y,Z),Z)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,X),f(Y,f(X,Y))) )).
