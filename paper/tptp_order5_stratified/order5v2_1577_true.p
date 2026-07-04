% order5v2_1577  eq1=42373 eq2=4329  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( f(X,Y) = f(Z,f(W,f(U,f(X,U)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,X)) = f(Z,f(X,W)) )).
