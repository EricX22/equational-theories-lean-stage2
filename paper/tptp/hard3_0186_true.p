% hard3_0186  eq1=1663 eq2=214  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(X,Y),f(f(Y,Z),W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(Y,Z)),X) )).
