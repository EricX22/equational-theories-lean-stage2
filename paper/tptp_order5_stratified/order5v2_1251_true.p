% order5v2_1251  eq1=27120 eq2=48088  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,W)),f(U,Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Y,f(Y,Z)),f(Z,Y)) )).
