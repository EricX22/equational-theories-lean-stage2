% order5v2_1687  eq1=15884 eq2=38581  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,f(Z,X)),Y),Z)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(f(Y,f(f(Z,X),W)),X),U) )).
