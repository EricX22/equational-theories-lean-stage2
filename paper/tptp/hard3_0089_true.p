% hard3_0089  eq1=652 eq2=3266  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(X,f(Y,f(f(Z,X),W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(X,f(Y,f(Z,Z))) )).
