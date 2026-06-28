% hard3_0216  eq1=2048 eq2=4512  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,X),Y),f(Z,Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(X,Y),Z) )).
