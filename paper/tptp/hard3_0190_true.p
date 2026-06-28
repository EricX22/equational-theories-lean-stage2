% hard3_0190  eq1=1682 eq2=4515  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(Y,X),f(f(X,X),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(X,Z),Y) )).
