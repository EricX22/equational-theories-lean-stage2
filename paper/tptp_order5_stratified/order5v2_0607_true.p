% order5v2_0607  eq1=23940 eq2=15027  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(W,f(Z,U))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,Z),f(Y,Z)),Y)) )).
