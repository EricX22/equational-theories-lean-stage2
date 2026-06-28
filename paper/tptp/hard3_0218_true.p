% hard3_0218  eq1=2059 eq2=462  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,Y),X),f(Z,W)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(X,f(Y,f(Z,f(W,U)))) )).
