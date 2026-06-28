% hard3_0257  eq1=2430 eq2=2746  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(W,W))),X) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(Y,Y),f(Y,Y)),X) )).
