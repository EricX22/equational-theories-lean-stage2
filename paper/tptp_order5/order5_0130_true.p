% order5_0130  eq1=20967 eq2=42236  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(f(f(Z,W),Y),Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(Z,f(Z,f(W,Z)))) )).
