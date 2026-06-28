% hard3_0114  eq1=922 eq2=1444  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Y,Y),f(Z,X))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,Y),f(X,f(Y,X))) )).
