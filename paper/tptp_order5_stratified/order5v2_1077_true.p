% order5v2_1077  eq1=1600 eq2=57806  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(Z,f(W,Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,Y)) = f(f(f(Z,W),Z),Z) )).
