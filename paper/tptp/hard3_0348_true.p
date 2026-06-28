% hard3_0348  eq1=3280 eq2=3777  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(Y,f(Y,f(X,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Y,Z),f(Z,Y)) )).
