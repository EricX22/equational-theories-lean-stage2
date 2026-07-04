% order5v2_0952  eq1=21636 eq2=22674  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(X,Z)),f(X,f(X,Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(Y,Z)),f(f(X,Z),W)) )).
