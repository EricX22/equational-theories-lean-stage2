% hard3_0376  eq1=3791 eq2=4283  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(Z,X),f(Y,Z)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(X,Y)) = f(X,f(Y,X)) )).
