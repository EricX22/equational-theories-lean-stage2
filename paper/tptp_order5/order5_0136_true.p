% order5_0136  eq1=57265 eq2=47163  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(W,f(W,Z)),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Y,X),f(f(Y,Z),Z)) )).
