% order5v2_0290  eq1=19090 eq2=53356  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(f(X,X),f(Z,W))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(f(Y,Y),Z),W),W) )).
