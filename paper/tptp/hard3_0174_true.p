% hard3_0174  eq1=1539 eq2=2521  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Y),f(Z,f(Y,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(f(X,Z),Z)),X) )).
