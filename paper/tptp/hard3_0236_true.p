% hard3_0236  eq1=2126 eq2=1691  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Y),X),f(X,Z)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(Y,X),f(f(Y,X),X)) )).
