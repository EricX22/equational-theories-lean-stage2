% order5v2_1307  eq1=26603 eq2=59025  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,f(f(Z,W),U)),f(W,Z)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(f(X,Y),Z) = f(W,f(W,f(W,U))) )).
