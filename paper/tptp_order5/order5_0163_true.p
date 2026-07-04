% order5_0163  eq1=10510 eq2=8338  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,X),f(f(Z,W),Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(Y,f(f(f(Z,X),Z),Y))) )).
