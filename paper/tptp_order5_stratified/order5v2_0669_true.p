% order5v2_0669  eq1=36971 eq2=59358  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Z),f(Z,Z)),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,Y),X) = f(Z,f(f(X,W),X)) )).
