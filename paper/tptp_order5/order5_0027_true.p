% order5_0027  eq1=43353 eq2=9354  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(Y,f(f(X,Y),f(Z,Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(X,Y),f(Z,f(W,Z)))) )).
