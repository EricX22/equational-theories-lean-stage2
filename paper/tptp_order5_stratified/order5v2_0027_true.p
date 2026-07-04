% order5v2_0027  eq1=2219 eq2=22624  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(Y,Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(Y,X)),f(f(Z,W),W)) )).
