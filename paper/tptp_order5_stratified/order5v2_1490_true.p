% order5v2_1490  eq1=26412 eq2=35764  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(f(Z,Z),X)),f(Z,Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,f(Y,X)),f(Z,X)),X) )).
