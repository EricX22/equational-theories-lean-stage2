% order5v2_0312  eq1=51667 eq2=49341  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Y,Z),f(W,Z)),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Z,W),Z),f(Y,W)) )).
