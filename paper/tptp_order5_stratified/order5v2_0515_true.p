% order5v2_0515  eq1=21866 eq2=53697  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,X)),f(X,f(X,W))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(f(Z,W),Y),Y),X) )).
