% order5_0120  eq1=14778 eq2=30458  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,Z),f(X,Z)),X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(X,f(f(Z,W),X))),Z) )).
