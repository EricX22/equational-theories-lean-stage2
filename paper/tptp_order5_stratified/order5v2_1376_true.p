% order5v2_1376  eq1=18704 eq2=43925  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(f(U,Z),Z))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(Y,W),f(Y,U))) )).
