% order5_0187  eq1=2830 eq2=59525  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,Y)),U) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,Y),Y) = f(Z,f(f(Y,Z),W)) )).
