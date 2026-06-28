% hard3_0289  eq1=2693 eq2=422  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(Z,W)),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(X,f(Y,f(Z,X)))) )).
