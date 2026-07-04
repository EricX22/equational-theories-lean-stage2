% order5_0157  eq1=55504 eq2=47782  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(W,f(f(W,Y),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(Y,f(Y,Z)),f(Y,Y)) )).
