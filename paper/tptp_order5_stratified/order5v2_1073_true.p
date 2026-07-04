% order5v2_1073  eq1=49195 eq2=57472  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Z,Y),W),f(W,Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(X,Y)) = f(f(f(Z,Y),W),Z) )).
