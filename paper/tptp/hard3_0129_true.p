% hard3_0129  eq1=1034 eq2=4630  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(X,f(f(X,f(Y,Z)),W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,Y),X) = f(f(X,Y),Z) )).
