% hard3_0369  eq1=3676 eq2=4682  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(f(Y,X),f(X,Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,Y),Z) = f(f(Y,W),Z) )).
