% hard3_0016  eq1=62 eq2=3762  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,f(X,f(X,X))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(Y,Y),f(Y,Y)) )).
