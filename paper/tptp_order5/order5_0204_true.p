% order5_0204  eq1=318 eq2=24161  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(Y,f(Z,X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(X,Y),Z),f(f(Z,W),X)) )).
