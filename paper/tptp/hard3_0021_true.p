% hard3_0021  eq1=100 eq2=845  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(X,f(f(X,X),Y)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(f(Y,Y),f(Y,X))) )).
