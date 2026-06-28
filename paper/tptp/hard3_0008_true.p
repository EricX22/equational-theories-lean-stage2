% hard3_0008  eq1=41 eq2=4407  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(Y,Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(X,Y)) = f(f(Y,X),Z) )).
