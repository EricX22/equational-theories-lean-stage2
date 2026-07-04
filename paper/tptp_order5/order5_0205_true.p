% order5_0205  eq1=45574 eq2=15559  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(f(X,Y),W),W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(f(X,f(Z,W)),Z),Z)) )).
