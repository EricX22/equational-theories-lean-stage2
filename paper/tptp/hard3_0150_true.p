% hard3_0150  eq1=1243 eq2=1067  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(f(Y,X),Y),Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(f(Y,f(Z,W)),X)) )).
