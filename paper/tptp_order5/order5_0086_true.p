% order5_0086  eq1=20755 eq2=27668  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,X),f(f(f(Y,Z),W),Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(X,f(Y,Z)),Z),f(Z,W)) )).
