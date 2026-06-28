% hard3_0056  eq1=366 eq2=4288  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(f(Y,X),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(X,Y)) = f(X,f(Z,Z)) )).
