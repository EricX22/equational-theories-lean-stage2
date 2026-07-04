% order5_0002  eq1=40162 eq2=61803  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,f(Y,X)),Z),W),Y) )).
fof(goal, conjecture, ! [X,Y] : ( f(f(X,X),Y) = f(f(f(Y,Y),Y),Y) )).
