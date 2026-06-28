% hard3_0058  eq1=373 eq2=359  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(f(Y,Z),W) )).
fof(goal, conjecture, ! [X] : ( f(X,X) = f(f(X,X),X) )).
