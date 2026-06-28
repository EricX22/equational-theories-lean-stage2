% hard3_0386  eq1=4110 eq2=359  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(f(f(Y,Z),Z),Z) )).
fof(goal, conjecture, ! [X] : ( f(X,X) = f(f(X,X),X) )).
