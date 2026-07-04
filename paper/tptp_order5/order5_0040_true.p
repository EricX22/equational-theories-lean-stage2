% order5_0040  eq1=29201 eq2=25427  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),W),f(Z,W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(X,W))),f(Y,X)) )).
