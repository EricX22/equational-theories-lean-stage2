% order5v2_0418  eq1=31525 eq2=14613  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,X),f(X,W))),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(f(X,Y),f(Z,Z)),W)) )).
