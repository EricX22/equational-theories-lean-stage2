% hard3_0020  eq1=90 eq2=1428  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Z,f(Z,X))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,X),f(X,f(Y,X))) )).
