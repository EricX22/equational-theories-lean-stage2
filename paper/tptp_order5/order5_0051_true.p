% order5_0051  eq1=48447 eq2=50771  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(W,Y)),f(W,Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Y,f(f(Z,Z),Z)),Z) )).
