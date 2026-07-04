% order5_0010  eq1=15649 eq2=54813  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,f(Z,X)),X),Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(X,Y)) = f(Z,f(f(X,X),W)) )).
