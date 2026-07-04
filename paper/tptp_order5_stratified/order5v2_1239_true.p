% order5v2_1239  eq1=15549 eq2=16404  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(f(X,f(Z,W)),X),Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(f(f(X,Z),Y),W),Z)) )).
