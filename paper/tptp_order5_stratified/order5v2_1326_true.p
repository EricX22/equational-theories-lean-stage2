% order5v2_1326  eq1=38610 eq2=27076  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(f(Z,Y),X)),Y),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,Y)),f(Z,W)) )).
