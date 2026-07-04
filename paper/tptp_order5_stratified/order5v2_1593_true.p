% order5v2_1593  eq1=27288 eq2=6742  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(Z,X)),f(Z,Y)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(Y,f(X,f(f(Z,X),f(W,U)))) )).
