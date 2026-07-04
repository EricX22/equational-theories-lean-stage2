% order5v2_1484  eq1=6392 eq2=26409  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(W,f(f(W,Y),Y)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,Z),X)),f(Y,W)) )).
