% hard3_0385  eq1=4099 eq2=359  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(f(f(Y,Y),Z),W) )).
fof(goal, conjecture, ! [X] : ( f(X,X) = f(f(X,X),X) )).
