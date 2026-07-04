% order5_0072  eq1=6329 eq2=26415  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(W,f(f(X,U),Y)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,Z),X)),f(W,Y)) )).
