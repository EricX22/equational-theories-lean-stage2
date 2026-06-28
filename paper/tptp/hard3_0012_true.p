% hard3_0012  eq1=52 eq2=3664  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(X,f(Y,f(X,X))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(f(X,Y),f(X,X)) )).
