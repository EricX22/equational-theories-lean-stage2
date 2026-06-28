% hard3_0310  eq1=2889 eq2=27  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,f(Y,Z)),Y),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,Y),Z) )).
