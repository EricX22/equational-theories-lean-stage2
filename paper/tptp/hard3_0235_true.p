% hard3_0235  eq1=2126 eq2=1071  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Y),X),f(X,Z)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(X,f(f(Y,f(Z,W)),U)) )).
