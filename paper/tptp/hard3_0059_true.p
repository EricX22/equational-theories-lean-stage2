% hard3_0059  eq1=373 eq2=4416  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(f(Y,Z),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(X,Y)) = f(f(Z,X),Y) )).
