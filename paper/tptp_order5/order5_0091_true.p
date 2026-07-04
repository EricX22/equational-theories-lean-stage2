% order5_0091  eq1=42376 eq2=57788  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( f(X,Y) = f(Z,f(W,f(U,f(Y,Y)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,Y)) = f(f(f(Z,Z),Z),W) )).
