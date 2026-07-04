% order5v2_0846  eq1=53511 eq2=4418  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,V,W,X,Y,Z] : ( f(X,Y) = f(f(f(f(Z,X),W),U),V) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(X,Y)) = f(f(Z,X),W) )).
