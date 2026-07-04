% order5v2_0633  eq1=28210 eq2=34966  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,Z)),W),f(X,W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Y),f(f(Z,Y),Z)),X) )).
