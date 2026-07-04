% order5v2_0367  eq1=49627 eq2=55222  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(X,f(X,f(X,X))),Z) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,f(Y,Z)) = f(X,f(f(Y,W),U)) )).
