% hard3_0359  eq1=3483 eq2=3766  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(Y,f(f(Y,X),Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Y,Y),f(Z,Z)) )).
