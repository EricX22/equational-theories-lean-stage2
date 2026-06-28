% hard3_0222  eq1=2081 eq2=656  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,Y),Z),f(Z,W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(Y,f(f(Z,Y),W))) )).
