% order5_0186  eq1=12701 eq2=53707  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Y,f(Z,Y))),X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(f(Z,W),Y),W),X) )).
