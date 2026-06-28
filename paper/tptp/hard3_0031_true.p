% hard3_0031  eq1=156 eq2=3334  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(X,Y),f(X,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(Z,f(Z,Y))) )).
