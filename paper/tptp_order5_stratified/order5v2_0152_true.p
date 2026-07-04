% order5v2_0152  eq1=22510 eq2=35472  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(X,Y)),f(f(Z,W),W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,f(Y,X)),f(Z,Z)),Z) )).
