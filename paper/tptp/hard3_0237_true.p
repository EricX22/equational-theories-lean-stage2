% hard3_0237  eq1=2126 eq2=3734  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Y),X),f(X,Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(X,Z),f(X,W)) )).
