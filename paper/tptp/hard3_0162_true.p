% hard3_0162  eq1=1462 eq2=4135  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,Y),f(Z,f(X,Y))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(f(X,Y),Z),Z) )).
