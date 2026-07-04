% order5v2_0649  eq1=23965 eq2=61001  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(U,f(Z,Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,X),Y) = f(f(Z,f(W,X)),Y) )).
