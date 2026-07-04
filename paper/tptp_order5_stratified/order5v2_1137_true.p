% order5v2_1137  eq1=33560 eq2=3847  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(f(Z,W),Z),Z)),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,W),f(Z,Y)) )).
