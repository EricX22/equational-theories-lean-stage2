% order5v2_1441  eq1=36063 eq2=5168  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,Z)),f(X,W)),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(Y,f(Z,f(Z,f(Z,W))))) )).
