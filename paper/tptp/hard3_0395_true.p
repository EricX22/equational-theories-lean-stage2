% hard3_0395  eq1=4545 eq2=4279  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(Z,Y),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(X,X)) = f(Y,f(Z,Y)) )).
