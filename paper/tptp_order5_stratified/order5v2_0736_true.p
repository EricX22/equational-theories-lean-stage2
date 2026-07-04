% order5v2_0736  eq1=279 eq2=7559  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,X),Z),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(X,f(f(X,f(Z,Z)),Z))) )).
