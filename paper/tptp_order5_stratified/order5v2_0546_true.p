% order5v2_0546  eq1=19917 eq2=20791  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,X),f(f(Z,f(Z,X)),Z)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(Y,X),f(f(f(Z,Y),W),U)) )).
