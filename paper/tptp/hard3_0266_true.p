% hard3_0266  eq1=2521 eq2=1879  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(f(X,Z),Z)),X) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,f(Y,Z)),f(W,X)) )).
