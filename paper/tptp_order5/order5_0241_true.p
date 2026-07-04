% order5_0241  eq1=42290 eq2=54172  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,V,W,X,Y,Z] : ( f(X,Y) = f(Z,f(W,f(X,f(U,V)))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(Y,Y)) = f(X,f(Y,f(X,Y))) )).
