% order5v2_1830  eq1=19991 eq2=38487  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(f(X,f(Z,W)),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,f(f(Y,Z),Z)),Y),X) )).
