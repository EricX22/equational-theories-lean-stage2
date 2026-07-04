% order5_0119  eq1=57061 eq2=52242  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(Y,f(Z,Y)),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,X) = f(f(f(Y,f(Z,W)),Z),Z) )).
