% order5v2_1038  eq1=19443 eq2=25841  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(Z,W),f(Y,Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,f(f(Y,Y),X)),f(Z,W)) )).
