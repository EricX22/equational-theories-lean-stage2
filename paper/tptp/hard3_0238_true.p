% hard3_0238  eq1=2144 eq2=1734  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Y),Z),f(X,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,Y),f(f(Y,Z),X)) )).
