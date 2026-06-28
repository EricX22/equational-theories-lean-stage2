% hard3_0063  eq1=423 eq2=1070  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(X,f(Y,f(Z,Y)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(f(Y,f(Z,W)),W)) )).
