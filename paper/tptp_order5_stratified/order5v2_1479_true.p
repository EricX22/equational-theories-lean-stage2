% order5v2_1479  eq1=303 eq2=19715  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),W),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,Y),f(f(Y,f(Z,X)),Z)) )).
