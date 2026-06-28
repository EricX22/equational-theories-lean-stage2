% hard3_0280  eq1=2675 eq2=3312  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,Y),f(Y,Z)),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(X,f(Z,Y))) )).
