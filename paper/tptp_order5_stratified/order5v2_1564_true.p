% order5v2_1564  eq1=37564 eq2=49343  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,f(Y,f(Y,Z))),Z),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Z,W),Z),f(Z,X)) )).
