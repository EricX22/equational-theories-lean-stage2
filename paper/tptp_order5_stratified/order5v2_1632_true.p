% order5v2_1632  eq1=32102 eq2=6185  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(f(X,f(X,Y)),Z)),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(Y,f(f(Y,W),Z)))) )).
