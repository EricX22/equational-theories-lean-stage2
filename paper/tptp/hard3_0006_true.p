% hard3_0006  eq1=38 eq2=4271  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( f(X,X) = f(X,Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(X,X)) = f(X,f(Y,Z)) )).
