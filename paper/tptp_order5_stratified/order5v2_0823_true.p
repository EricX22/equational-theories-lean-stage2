% order5v2_0823  eq1=39467 eq2=49459  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),f(X,W)),Z),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(X,f(Y,f(Z,X))),Z) )).
