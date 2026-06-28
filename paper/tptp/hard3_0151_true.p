% hard3_0151  eq1=1243 eq2=4583  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(f(Y,X),Y),Z)) )).
fof(goal, conjecture, ! [X,Y] : ( f(f(X,X),X) = f(f(X,X),Y) )).
