% order5_0012  eq1=32605 eq2=46306  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,f(Z,W)),Z)),W) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(Y,Y),f(X,f(X,Y))) )).
