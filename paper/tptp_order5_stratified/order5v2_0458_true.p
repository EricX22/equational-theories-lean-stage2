% order5v2_0458  eq1=40603 eq2=24303  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,f(Z,W)),W),Z),U) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,X),Z),f(f(Z,X),W)) )).
