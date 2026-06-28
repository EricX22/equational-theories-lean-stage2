% hard3_0086  eq1=646 eq2=4144  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(Y,f(f(Y,Z),Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(X,Z),Y),W) )).
