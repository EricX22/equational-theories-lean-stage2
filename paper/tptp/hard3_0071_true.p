% hard3_0071  eq1=511 eq2=2132  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,f(Y,f(Y,f(X,Y)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Y),X),f(Z,Z)) )).
