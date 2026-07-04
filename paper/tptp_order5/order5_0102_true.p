% order5_0102  eq1=3580 eq2=18898  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(Y,f(f(Z,W),W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,Y),f(f(Z,Z),f(Z,W))) )).
