% hard3_0370  eq1=3683 eq2=3593  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(f(Y,X),f(Z,W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(X,Z),W)) )).
