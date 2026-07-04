% order5_0145  eq1=20825 eq2=38113  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,X),f(f(f(Z,W),W),Y)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,f(f(Y,Y),X)),Y),X) )).
