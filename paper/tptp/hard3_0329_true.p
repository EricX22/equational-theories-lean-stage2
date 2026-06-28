% hard3_0329  eq1=3074 eq2=4288  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(X,Y),X),Z),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(X,Y)) = f(X,f(Z,Z)) )).
