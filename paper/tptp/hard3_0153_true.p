% hard3_0153  eq1=1259 eq2=4318  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(f(Y,Z),X),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,X)) = f(X,f(Z,Z)) )).
