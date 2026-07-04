% order5_0230  eq1=50202 eq2=6023  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(W,f(Y,W))),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(Y,f(Z,f(f(Y,Y),Z)))) )).
