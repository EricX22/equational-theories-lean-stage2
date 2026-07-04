% order5_0129  eq1=35683 eq2=3687  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,f(X,Z)),f(X,W)),U) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(f(Y,Y),f(Y,X)) )).
