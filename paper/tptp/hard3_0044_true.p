% hard3_0044  eq1=269 eq2=3949  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,Y),Z),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(X,f(Z,W)),W) )).
