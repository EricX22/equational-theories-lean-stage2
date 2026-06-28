% hard3_0281  eq1=2678 eq2=417  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(Y,Z)),W) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(X,f(Y,f(X,Y)))) )).
