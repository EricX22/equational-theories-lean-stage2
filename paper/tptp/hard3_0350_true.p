% hard3_0350  eq1=3291 eq2=4480  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(Z,f(X,W))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(Y,Y)) = f(f(Y,X),Y) )).
