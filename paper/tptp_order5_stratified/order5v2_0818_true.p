% order5v2_0818  eq1=11436 eq2=56587  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,f(Y,Y)),f(X,W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(X,Y)) = f(f(Z,f(Y,Y)),Z) )).
