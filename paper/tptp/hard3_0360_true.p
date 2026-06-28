% hard3_0360  eq1=3490 eq2=355  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(f(Y,Z),W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(W,Y)) )).
