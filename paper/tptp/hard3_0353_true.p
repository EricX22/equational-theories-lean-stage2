% hard3_0353  eq1=3349 eq2=4682  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(Y,f(X,f(Z,Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,Y),Z) = f(f(Y,W),Z) )).
