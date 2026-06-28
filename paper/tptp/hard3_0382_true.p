% hard3_0382  eq1=3946 eq2=4339  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(X,f(Z,W)),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,Y)) = f(X,f(Y,Z)) )).
