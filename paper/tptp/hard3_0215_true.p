% hard3_0215  eq1=2046 eq2=1063  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,X),Y),f(Z,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Z,Z)),X)) )).
