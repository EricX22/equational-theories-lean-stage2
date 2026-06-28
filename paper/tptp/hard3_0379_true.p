% hard3_0379  eq1=3857 eq2=4316  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( f(X,Y) = f(f(Z,W),f(U,Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,X)) = f(X,f(Z,X)) )).
