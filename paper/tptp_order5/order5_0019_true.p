% order5_0019  eq1=4389 eq2=51601  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( f(X,f(X,X)) = f(f(Y,Y),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Y,Y),f(Z,W)),Z) )).
