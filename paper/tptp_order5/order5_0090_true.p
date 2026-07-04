% order5_0090  eq1=22118 eq2=42457  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,f(Z,W)),f(X,f(U,U))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,X) = f(X,f(Y,f(f(Z,W),U))) )).
