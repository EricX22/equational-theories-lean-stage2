% order5v2_0913  eq1=24231 eq2=22793  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,X),Y),f(f(X,X),Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,X)),f(f(W,X),Z)) )).
