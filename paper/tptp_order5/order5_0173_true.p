% order5_0173  eq1=44211 eq2=24697  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( f(X,X) = f(X,f(f(Y,f(Z,W)),U)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),Z),f(f(Z,W),W)) )).
