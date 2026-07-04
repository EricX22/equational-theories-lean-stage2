% order5_0248  eq1=57834 eq2=9682  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(f(X,X),W),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,Y),f(Y,f(X,W)))) )).
