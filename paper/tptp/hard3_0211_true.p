% hard3_0211  eq1=1979 eq2=4351  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(Z,Y)),f(Y,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,Y)) = f(Z,f(Y,Y)) )).
