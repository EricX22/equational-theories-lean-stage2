% order5_0041  eq1=37740 eq2=53967  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,f(Y,X))),W),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(X,Y)) = f(Z,f(Z,f(X,X))) )).
