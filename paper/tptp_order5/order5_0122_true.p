% order5_0122  eq1=25062 eq2=58519  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(X,f(Y,f(Z,W))),f(W,U)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(f(X,Y),X) = f(Z,f(Z,f(W,U))) )).
