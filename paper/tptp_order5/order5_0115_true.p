% order5_0115  eq1=41477 eq2=1111  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(f(Y,Z),W),W),Z),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(Y,f(X,X)),Z)) )).
