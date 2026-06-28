% hard3_0030  eq1=155 eq2=3509  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,X),f(Y,Z)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(X,f(f(X,X),Y)) )).
