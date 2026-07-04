% order5v2_0578  eq1=49714 eq2=55572  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(X,f(Z,f(X,W))),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(X,X)) = f(f(X,Y),f(Z,X)) )).
