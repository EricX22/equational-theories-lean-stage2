% order5_0076  eq1=27977 eq2=42370  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Y,Z)),W),f(X,Y)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,Y) = f(Z,f(W,f(U,f(X,Y)))) )).
