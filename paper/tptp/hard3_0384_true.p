% hard3_0384  eq1=4088 eq2=3700  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(f(f(Y,X),Z),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(Y,Z),f(Y,Z)) )).
